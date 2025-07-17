// components/EvidenceTracker.tsx
"use client";
import React, { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';
import { Search, Filter, Download, UserPlus, ChevronLeft, ChevronRight, Users, Building } from 'lucide-react';
import AuditButton from './AuditButton';

// Supabase client setup
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

// Only create Supabase client if environment variables are available
let supabase: any = null;
if (supabaseUrl && supabaseKey && supabaseUrl !== 'https://your-project.supabase.co') {
  supabase = createClient(supabaseUrl, supabaseKey);
}

// Types
interface RequirementStatusItem {
  id: string;
  requirement_id: string;
  requirement_description: string;
  status: 'compliant' | 'non_compliant' | 'pending' | 'not_applicable';
  aws_account_id: string;
  control_id: string;
  last_evaluated: string;
  evidence_url?: string;
  remediation_notes?: string;
  created_at: string;
  updated_at: string;
}

interface UserAccount {
  id: string;
  auditor_id: string;
  aws_account_id: string;
  account_name: string;
  status: string;
}

interface StatusCounts {
  compliant: number;
  non_compliant: number;
  pending: number;
  not_applicable: number;
  total: number;
}

const EvidenceTracker: React.FC = () => {
  const [requirementData, setRequirementData] = useState<RequirementStatusItem[]>([]);
  const [filteredData, setFilteredData] = useState<RequirementStatusItem[]>([]);
  const [userAccounts, setUserAccounts] = useState<UserAccount[]>([]);
  const [statusCounts, setStatusCounts] = useState<StatusCounts>({
    compliant: 0,
    non_compliant: 0,
    pending: 0,
    not_applicable: 0,
    total: 0
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [selectedAuditor, setSelectedAuditor] = useState<string>('');
  const [selectedAwsAccount, setSelectedAwsAccount] = useState<string>('');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [auditorAccounts, setAuditorAccounts] = useState<UserAccount[]>([]);
  const itemsPerPage = 10;

  // Add this function inside your EvidenceTracker component
  const getPaginationPages = (): number[] => {
    const pages: number[] = [];
    const maxVisiblePages = 5;
    
    if (totalPages <= maxVisiblePages) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      const halfVisible = Math.floor(maxVisiblePages / 2);
      let startPage = Math.max(1, currentPage - halfVisible);
      let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
      
      if (endPage - startPage < maxVisiblePages - 1) {
        startPage = Math.max(1, endPage - maxVisiblePages + 1);
      }
      
      if (startPage > 1) {
        pages.push(1);
        if (startPage > 2) {
          pages.push(-1);
        }
      }
      
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }
      
      if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
          pages.push(-1);
        }
        pages.push(totalPages);
      }
    }
    
    return pages;
  };

  // Fetch auditor accounts and user accounts
  useEffect(() => {
    fetchUserAccounts();
  }, []);

  // Fetch requirement data when selections change
  useEffect(() => {
    if (selectedAwsAccount) {
      fetchRequirementData();
    } else {
      setRequirementData([]);
      setFilteredData([]);
      resetStatusCounts();
    }
  }, [selectedAwsAccount]);

  // Filter data based on search
  useEffect(() => {
    if (!searchTerm) {
      setFilteredData(requirementData);
    } else {
      const filtered = requirementData.filter(item => 
        item.requirement_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.requirement_description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.control_id.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredData(filtered);
    }
    setCurrentPage(1);
  }, [requirementData, searchTerm]);

  const fetchUserAccounts = async () => {
    try {
      setLoading(true);
      
      const { data, error } = await supabase
        .from('user_accounts')
        .select('*')
        .order('auditor_id', { ascending: true });

      if (error) throw error;

      setUserAccounts(data);
      
      // Get unique auditors
      const uniqueAuditors = [...new Set(data.map(account => account.auditor_id))];
      if (uniqueAuditors.length > 0 && !selectedAuditor) {
        setSelectedAuditor(uniqueAuditors[0]);
        updateAuditorAccounts(uniqueAuditors[0], data);
      }
    } catch (error) {
      console.error('Error fetching user accounts:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateAuditorAccounts = (auditorId: string, accounts: UserAccount[]) => {
    const filteredAccounts = accounts.filter(account => account.auditor_id === auditorId);
    setAuditorAccounts(filteredAccounts);
    
    // Auto-select first account if none selected
    if (filteredAccounts.length > 0 && !selectedAwsAccount) {
      setSelectedAwsAccount(filteredAccounts[0].aws_account_id);
    }
  };

  const fetchRequirementData = async () => {
    if (!selectedAwsAccount) return;
    
    try {
      setLoading(true);
      
      const { data, error } = await supabase
        .from('requirement_status')
        .select('*')
        .eq('aws_account_id', selectedAwsAccount)
        .order('requirement_id', { ascending: true });

      if (error) throw error;

      setRequirementData(data);
      calculateStatusCounts(data);
    } catch (error) {
      console.error('Error fetching requirement data:', error);
      setRequirementData([]);
      resetStatusCounts();
    } finally {
      setLoading(false);
    }
  };

  const calculateStatusCounts = (data: RequirementStatusItem[]) => {
    const counts = data.reduce((acc, item) => {
      acc[item.status] = (acc[item.status] || 0) + 1;
      return acc;
    }, { compliant: 0, non_compliant: 0, pending: 0, not_applicable: 0 });

    setStatusCounts({
      compliant: counts.compliant || 0,
      non_compliant: counts.non_compliant || 0,
      pending: counts.pending || 0,
      not_applicable: counts.not_applicable || 0,
      total: data.length
    });
  };

  const resetStatusCounts = () => {
    setStatusCounts({
      compliant: 0,
      non_compliant: 0,
      pending: 0,
      not_applicable: 0,
      total: 0
    });
  };

  const handleAuditorChange = (auditorId: string) => {
    setSelectedAuditor(auditorId);
    updateAuditorAccounts(auditorId, userAccounts);
    setSelectedAwsAccount(''); // Reset AWS account selection
  };

  const handleAwsAccountChange = (accountId: string) => {
    setSelectedAwsAccount(accountId);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'compliant':
        return 'bg-green-100 text-green-800 border border-green-200';
      case 'non_compliant':
        return 'bg-red-100 text-red-800 border border-red-200';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 border border-yellow-200';
      case 'not_applicable':
        return 'bg-secondary text-secondary-foreground border';
      default:
        return 'bg-secondary text-secondary-foreground border';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'compliant':
        return '✅';
      case 'non_compliant':
        return '❌';
      case 'pending':
        return '⏳';
      case 'not_applicable':
        return '➖';
      default:
        return '❓';
    }
  };

  const getStatusDisplayName = (status: string) => {
    switch (status) {
      case 'compliant':
        return 'Compliant';
      case 'non_compliant':
        return 'Non-Compliant';
      case 'pending':
        return 'Pending';
      case 'not_applicable':
        return 'Not Applicable';
      default:
        return status;
    }
  };

  // Pagination calculations
  const totalPages = Math.ceil(filteredData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentData = filteredData.slice(startIndex, endIndex);

  const goToPage = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  // Handle audit completion
// In your EvidenceTracker component, replace the handleAuditComplete function:

const handleAuditComplete = async (controlId: string, auditResult: any) => {
  console.log('📊 Audit completed for control:', controlId);
  console.log('📋 Audit result:', auditResult);
  
  // Simple success/failure notification based on API response
  if (auditResult.success) {
    console.log(`✅ Audit successful for control ${controlId}`);
    
    // Show success notification to user
    alert(`✅ Audit completed successfully for control ${controlId}!\n\nThe database has been updated with the latest compliance status.`);
    
    // Refresh the data to show any updated status from database
    await fetchRequirementData();
    
  } else {
    console.log(`❌ Audit failed for control ${controlId}`);
    console.log('Error details:', auditResult.message || auditResult.error);
    
    // Show failure notification to user
    alert(`❌ Audit failed for control ${controlId}!\n\nReason: ${auditResult.message || 'Unknown error'}\n\nPlease try again or contact support.`);
  }
};

  const StatusCard = ({ title, count, icon, color }: { title: string; count: number; icon: string; color: string }) => (
    <div className={`${color} rounded-lg p-4 flex items-center justify-between min-w-[140px] border shadow-sm`}>
      <div>
        <div className="text-2xl font-bold">{count}</div>
        <div className="text-sm opacity-75">{title}</div>
      </div>
      <div className="text-2xl">{icon}</div>
    </div>
  );

  const uniqueAuditors = [...new Set(userAccounts.map(account => account.auditor_id))];

  return (
    <div className="min-h-screen w-full">
      {/* Header */}
      <div className="border-b p-4 shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">
              PCI DSS Compliance Auditor
            </h1>
            <p className="text-muted-foreground">
              PCI DSS ( v4.0.1 ) &gt;&gt; Requirements Audit Dashboard
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <button className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow-sm">
              <Download size={16} />
              <span>Export</span>
            </button>
            <button className="flex items-center space-x-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg shadow-sm">
              <UserPlus size={16} />
              <span>Assign</span>
            </button>
          </div>
        </div>
      </div>

      {/* Auditor and Account Selection */}
      <div className="p-6 border-b">
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-2">
            <Users size={20} className="text-muted-foreground" />
            <label className="text-sm font-medium">Auditor:</label>
            <select
              value={selectedAuditor}
              onChange={(e) => handleAuditorChange(e.target.value)}
              className="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">Select Auditor</option>
              {uniqueAuditors.map(auditorId => (
                <option key={auditorId} value={auditorId}>
                  {auditorId}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center space-x-2">
            <Building size={20} className="text-muted-foreground" />
            <label className="text-sm font-medium">AWS Account:</label>
            <select
              value={selectedAwsAccount}
              onChange={(e) => handleAwsAccountChange(e.target.value)}
              disabled={!selectedAuditor || auditorAccounts.length === 0}
              className="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary disabled:opacity-50"
            >
              <option value="">Select AWS Account</option>
              {auditorAccounts.map(account => (
                <option key={account.aws_account_id} value={account.aws_account_id}>
                  {account.account_name} ({account.aws_account_id})
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Status Cards */}
      <div className="p-6">
        <div className="flex space-x-4 mb-6 overflow-x-auto">
          <StatusCard
            title="Compliant"
            count={statusCounts.compliant}
            icon="✅"
            color="bg-primary/10 text-primary border-primary/20"
          />
          <StatusCard
            title="Non-Compliant"
            count={statusCounts.non_compliant}
            icon="❌"
            color="bg-primary/10 text-primary border-primary/20"
          />
          <StatusCard
            title="Pending"
            count={statusCounts.pending}
            icon="⏳"
            color="bg-primary/10 text-primary border-primary/20"
          />
          <StatusCard
            title="Not Applicable"
            count={statusCounts.not_applicable}
            icon="➖"
            color="bg-primary/10 text-primary border-primary/20"
          />
          <StatusCard
            title="Total Requirements"
            count={statusCounts.total}
            icon="📊"
            color="bg-primary/10 text-primary border-primary/20"
          />
        </div>

        {/* Search and Filter */}
        <div className="flex items-center space-x-4 mb-6">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search requirements..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <button className="flex items-center space-x-2 hover:bg-accent px-4 py-2 rounded-lg border shadow-sm">
            <Filter size={16} />
            <span>Filter</span>
          </button>
        </div>

        {/* Requirements Table */}
        <div className="rounded-lg overflow-hidden border">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-muted/50 border-b">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Control ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Description
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {loading ? (
                  <tr>
                    <td colSpan={4} className="px-6 py-4 text-center text-gray-500">
                      Loading...
                    </td>
                  </tr>
                ) : !selectedAwsAccount ? (
                  <tr>
                    <td colSpan={4} className="px-6 py-4 text-center text-muted-foreground">
                      Please select an auditor and AWS account to view requirements
                    </td>
                  </tr>
                ) : currentData.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="px-6 py-4 text-center text-muted-foreground">
                      {searchTerm ? "No matching requirements found" : "No requirements data found"}
                    </td>
                  </tr>
                ) : (
                  currentData.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="w-1 h-8 bg-blue-500 rounded-full mr-3"></div>
                          <div className="font-medium text-gray-900">
                            {item.control_id}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-700 max-w-md">
                          {item.requirement_description.length > 150
                            ? `${item.requirement_description.substring(0, 150)}...`
                            : item.requirement_description}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(item.status)}`}
                        >
                          {getStatusIcon(item.status)}{" "}
                          <span className="ml-1">{getStatusDisplayName(item.status)}</span>
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <div className="flex items-center space-x-4">
                          <span className="text-xs text-gray-400">
                            Last: {new Date(item.last_evaluated).toLocaleDateString()}
                          </span>
                          <AuditButton
                            requirementId={item.control_id}  // This passes "1.2.5" format
                            description={item.requirement_description}
                            onAuditComplete={(result) => handleAuditComplete(item.control_id, result)}
                            size="sm"
                            variant="outline"
                          />
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between mt-6">
            <div className="text-sm text-gray-500">
              Showing {startIndex + 1} to{" "}
              {Math.min(endIndex, filteredData.length)} of {filteredData.length}{" "}
              results
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => goToPage(currentPage - 1)}
                disabled={currentPage === 1}
                className="p-2 rounded border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed bg-white"
              >
                <ChevronLeft size={16} />
              </button>
              <div className="flex space-x-1">
                {getPaginationPages().map((page, index) =>
                  page === -1 ? (
                    <span
                      key={`ellipsis-${index}`}
                      className="px-3 py-1 text-gray-400"
                    >
                      ...
                    </span>
                  ) : (
                    <button
                      key={page}
                      className={`px-3 py-1 rounded text-sm transition-colors ${
                        currentPage === page
                          ? "bg-blue-600 text-white"
                          : "border border-gray-300 hover:bg-gray-50 bg-white text-gray-700"
                      }`}
                      onClick={() => goToPage(page)}
                    >
                      {page}
                    </button>
                  )
                )}
              </div>
              <button
                onClick={() => goToPage(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="p-2 rounded border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed bg-white"
              >
                <ChevronRight size={16} />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EvidenceTracker;