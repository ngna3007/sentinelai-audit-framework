// components/EvidenceTracker.tsx
'use client'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { createClient } from '@supabase/supabase-js'
import {
  BarChart3,
  Building,
  CheckCircle,
  ChevronLeft,
  ChevronRight,
  Clock,
  Download,
  FileText,
  Filter,
  Minus,
  Search,
  UserPlus,
  Users,
  XCircle
} from 'lucide-react'
import React, { useEffect, useState } from 'react'
import AuditButton from './AuditButton'

// Supabase client setup
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

// Only create Supabase client if environment variables are available
let supabase: any = null
if (supabaseUrl && supabaseKey && supabaseUrl !== 'https://your-project.supabase.co') {
  supabase = createClient(supabaseUrl, supabaseKey)
}

// Types
interface RequirementStatusItem {
  id: string
  requirement_id: string
  requirement_description: string
  status: 'compliant' | 'non_compliant' | 'pending' | 'not_applicable'
  aws_account_id: string
  control_id: string
  last_evaluated: string
  evidence_url?: string
  remediation_notes?: string
  created_at: string
  updated_at: string
}

interface UserAccount {
  id: string
  auditor_id: string
  aws_account_id: string
  account_name: string
  status: string
}

interface StatusCounts {
  compliant: number
  non_compliant: number
  pending: number
  not_applicable: number
  total: number
}

const EvidenceTracker: React.FC = () => {
  const [requirementData, setRequirementData] = useState<RequirementStatusItem[]>([])
  const [filteredData, setFilteredData] = useState<RequirementStatusItem[]>([])
  const [userAccounts, setUserAccounts] = useState<UserAccount[]>([])
  const [statusCounts, setStatusCounts] = useState<StatusCounts>({
    compliant: 0,
    non_compliant: 0,
    pending: 0,
    not_applicable: 0,
    total: 0
  })
  const [currentPage, setCurrentPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [selectedAuditor, setSelectedAuditor] = useState<string>('')
  const [selectedAwsAccount, setSelectedAwsAccount] = useState<string>('')
  const [searchTerm, setSearchTerm] = useState<string>('')
  const [auditorAccounts, setAuditorAccounts] = useState<UserAccount[]>([])
  const itemsPerPage = 10

  // Add this function inside your EvidenceTracker component
  const getPaginationPages = (): number[] => {
    const pages: number[] = []
    const maxVisiblePages = 5

    if (totalPages <= maxVisiblePages) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i)
      }
    } else {
      const halfVisible = Math.floor(maxVisiblePages / 2)
      let startPage = Math.max(1, currentPage - halfVisible)
      let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1)

      if (endPage - startPage < maxVisiblePages - 1) {
        startPage = Math.max(1, endPage - maxVisiblePages + 1)
      }

      if (startPage > 1) {
        pages.push(1)
        if (startPage > 2) {
          pages.push(-1)
        }
      }

      for (let i = startPage; i <= endPage; i++) {
        pages.push(i)
      }

      if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
          pages.push(-1)
        }
        pages.push(totalPages)
      }
    }

    return pages
  }

  // Fetch auditor accounts and user accounts
  useEffect(() => {
    fetchUserAccounts()
  }, [])

  // Fetch requirement data when selections change
  useEffect(() => {
    if (selectedAwsAccount) {
      fetchRequirementData()
    } else {
      setRequirementData([])
      setFilteredData([])
      resetStatusCounts()
    }
  }, [selectedAwsAccount])

  // Filter data based on search
  useEffect(() => {
    if (!searchTerm) {
      setFilteredData(requirementData)
    } else {
      const filtered = requirementData.filter(item =>
        item.requirement_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.requirement_description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.control_id.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredData(filtered)
    }
    setCurrentPage(1)
  }, [requirementData, searchTerm])

  const fetchUserAccounts = async () => {
    try {
      setLoading(true)

      const { data, error } = await supabase
        .from('user_accounts')
        .select('*')
        .order('auditor_id', { ascending: true })

      if (error) throw error

      setUserAccounts(data)

      // Get unique auditors
      const uniqueAuditors = [...new Set(data.map((account: UserAccount) => account.auditor_id))] as string[]
      if (uniqueAuditors.length > 0 && !selectedAuditor) {
        setSelectedAuditor(uniqueAuditors[0])
        updateAuditorAccounts(uniqueAuditors[0], data)
      }
    } catch (error) {
      console.error('Error fetching user accounts:', error)
    } finally {
      setLoading(false)
    }
  }

  const updateAuditorAccounts = (auditorId: string, accounts: UserAccount[]) => {
    const filteredAccounts = accounts.filter(account => account.auditor_id === auditorId)
    setAuditorAccounts(filteredAccounts)

    // Auto-select first account if none selected
    if (filteredAccounts.length > 0 && !selectedAwsAccount) {
      setSelectedAwsAccount(filteredAccounts[0].aws_account_id)
    }
  }

  const fetchRequirementData = async () => {
    if (!selectedAwsAccount) return

    try {
      setLoading(true)

      const { data, error } = await supabase
        .from('requirement_status')
        .select('*')
        .eq('aws_account_id', selectedAwsAccount)
        .order('requirement_id', { ascending: true })

      if (error) throw error

      setRequirementData(data)
      calculateStatusCounts(data)
    } catch (error) {
      console.error('Error fetching requirement data:', error)
      setRequirementData([])
      resetStatusCounts()
    } finally {
      setLoading(false)
    }
  }

  const calculateStatusCounts = (data: RequirementStatusItem[]) => {
    const counts = data.reduce((acc, item) => {
      acc[item.status] = (acc[item.status] || 0) + 1
      return acc
    }, { compliant: 0, non_compliant: 0, pending: 0, not_applicable: 0 })

    setStatusCounts({
      compliant: counts.compliant || 0,
      non_compliant: counts.non_compliant || 0,
      pending: counts.pending || 0,
      not_applicable: counts.not_applicable || 0,
      total: data.length
    })
  }

  const resetStatusCounts = () => {
    setStatusCounts({
      compliant: 0,
      non_compliant: 0,
      pending: 0,
      not_applicable: 0,
      total: 0
    })
  }

  const handleAuditorChange = (auditorId: string) => {
    setSelectedAuditor(auditorId)
    updateAuditorAccounts(auditorId, userAccounts)
    setSelectedAwsAccount('') // Reset AWS account selection
  }

  const handleAwsAccountChange = (accountId: string) => {
    setSelectedAwsAccount(accountId)
  }

  const getStatusVariant = (status: string) => {
    switch (status) {
      case 'compliant':
        return 'default'
      case 'non_compliant':
        return 'destructive'
      case 'pending':
        return 'secondary'
      case 'not_applicable':
        return 'outline'
      default:
        return 'outline'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'compliant':
        return <CheckCircle size={16} />
      case 'non_compliant':
        return <XCircle size={16} />
      case 'pending':
        return <Clock size={16} />
      case 'not_applicable':
        return <Minus size={16} />
      default:
        return <FileText size={16} />
    }
  }

  const getStatusDisplayName = (status: string) => {
    switch (status) {
      case 'compliant':
        return 'Compliant'
      case 'non_compliant':
        return 'Non-Compliant'
      case 'pending':
        return 'Pending'
      case 'not_applicable':
        return 'Not Applicable'
      default:
        return status
    }
  }

  // Pagination calculations
  const totalPages = Math.ceil(filteredData.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const currentData = filteredData.slice(startIndex, endIndex)

  const goToPage = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page)
    }
  }

  // Handle audit completion
  const handleAuditComplete = async (controlId: string, auditResult: any) => {
    console.log('📊 Audit completed for control:', controlId)
    console.log('📋 Audit result:', auditResult)

    // Simple success/failure notification based on API response
    if (auditResult.success) {
      console.log(`✅ Audit successful for control ${controlId}`)

      // Show success notification to user
      alert(`✅ Audit completed successfully for control ${controlId}!\n\nThe database has been updated with the latest compliance status.`)

      // Refresh the data to show any updated status from database
      await fetchRequirementData()

    } else {
      console.log(`❌ Audit failed for control ${controlId}`)
      console.log('Error details:', auditResult.message || auditResult.error)

      // Show failure notification to user
      alert(`❌ Audit failed for control ${controlId}!\n\nReason: ${auditResult.message || 'Unknown error'}\n\nPlease try again or contact support.`)
    }
  }

  const StatusCard = ({ title, count, icon }: { title: string; count: number; icon: React.ReactNode }) => (
    <div className='bg-muted/20 rounded border p-2'>
      <div className='flex items-center justify-between'>
        <div>
          <div className='text-lg font-bold'>{count}</div>
          <div className='text-xs text-muted-foreground'>{title}</div>
        </div>
        <div className='text-muted-foreground'>{icon}</div>
      </div>
    </div>
  )

  const uniqueAuditors = [...new Set(userAccounts.map(account => account.auditor_id))]

  return (
    <div className='w-full space-y-2'>
      {/* Header */}
      <div className='border-b pb-2'>
        <div className='flex items-center justify-between'>
          <div>
            <h1 className='text-xl font-bold'>
              PCI DSS Compliance Auditor
            </h1>
            <p className='text-xs text-muted-foreground'>
              PCI DSS ( v4.0.1 ) &gt;&gt; Requirements Audit Dashboard
            </p>
          </div>
          <div className='flex items-center space-x-2'>
            <Button variant='outline' size='sm' className='flex items-center space-x-1'>
              <Download size={14} />
              <span className='text-xs'>Export</span>
            </Button>
            <Button size='sm' className='flex items-center space-x-1'>
              <UserPlus size={14} />
              <span className='text-xs'>Assign</span>
            </Button>
          </div>
        </div>
      </div>

      {/* Auditor and Account Selection */}
      <div className='border-b pb-2'>
        <div className='flex items-center space-x-4'>
          <div className='flex items-center space-x-2'>
            <Users size={16} className='text-muted-foreground' />
            <label className='text-xs font-medium'>Auditor:</label>
            <Select value={selectedAuditor} onValueChange={handleAuditorChange}>
              <SelectTrigger className='w-[160px] h-8'>
                <SelectValue placeholder='Select Auditor' />
              </SelectTrigger>
              <SelectContent>
                {uniqueAuditors.map(auditorId => (
                  <SelectItem key={auditorId} value={auditorId}>
                    {auditorId}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className='flex items-center space-x-2'>
            <Building size={16} className='text-muted-foreground' />
            <label className='text-xs font-medium'>AWS Account:</label>
            <Select
              value={selectedAwsAccount}
              onValueChange={handleAwsAccountChange}
              disabled={!selectedAuditor || auditorAccounts.length === 0}
            >
              <SelectTrigger className='w-[240px] h-8' disabled={!selectedAuditor || auditorAccounts.length === 0}>
                <SelectValue placeholder='Select AWS Account' />
              </SelectTrigger>
              <SelectContent>
                {auditorAccounts.map(account => (
                  <SelectItem key={account.aws_account_id} value={account.aws_account_id}>
                    {account.account_name} ({account.aws_account_id})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      {/* Status Cards */}
      <div className='grid grid-cols-5 gap-2'>
        <StatusCard
          title='Compliant'
          count={statusCounts.compliant}
          icon={<CheckCircle size={16} className='text-green-600' />}
        />
        <StatusCard
          title='Non-Compliant'
          count={statusCounts.non_compliant}
          icon={<XCircle size={16} className='text-red-600' />}
        />
        <StatusCard
          title='Pending'
          count={statusCounts.pending}
          icon={<Clock size={16} className='text-yellow-600' />}
        />
        <StatusCard
          title='Not Applicable'
          count={statusCounts.not_applicable}
          icon={<Minus size={16} className='text-gray-600' />}
        />
        <StatusCard
          title='Total Requirements'
          count={statusCounts.total}
          icon={<BarChart3 size={16} className='text-blue-600' />}
        />
      </div>

      {/* Search and Filter */}
      <div className='border-b pb-2'>
        <div className='flex items-center space-x-2'>
          <div className='relative flex-1 max-w-sm'>
            <Search className='absolute left-2 top-2 h-4 w-4 text-muted-foreground' />
            <Input
              type='text'
              placeholder='Search requirements...'
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className='pl-8 h-8 text-sm'
            />
          </div>
          <Button variant='outline' size='sm' className='flex items-center space-x-1 h-8'>
            <Filter size={14} />
            <span className='text-xs'>Filter</span>
          </Button>
        </div>
      </div>

      {/* Requirements Table */}
      <div className='border rounded'>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className='text-xs font-medium'>Control ID</TableHead>
              <TableHead className='text-xs font-medium'>Description</TableHead>
              <TableHead className='text-xs font-medium'>Status</TableHead>
              <TableHead className='text-xs font-medium'>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={4} className='text-center text-muted-foreground text-sm py-4'>
                  Loading...
                </TableCell>
              </TableRow>
            ) : !selectedAwsAccount ? (
              <TableRow>
                <TableCell colSpan={4} className='text-center text-muted-foreground text-sm py-4'>
                  Please select an auditor and AWS account to view requirements
                </TableCell>
              </TableRow>
            ) : currentData.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className='text-center text-muted-foreground text-sm py-4'>
                  {searchTerm ? 'No matching requirements found' : 'No requirements data found'}
                </TableCell>
              </TableRow>
            ) : (
              currentData.map((item) => (
                <TableRow key={item.id}>
                  <TableCell className='py-2'>
                    <div className='flex items-center'>
                      <div className='w-1 h-6 bg-blue-500 rounded-full mr-2'></div>
                      <div className='font-medium text-sm'>
                        {item.control_id}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell className='py-2'>
                    <div className='text-sm max-w-md'>
                      {item.requirement_description.length > 120
                        ? `${item.requirement_description.substring(0, 120)}...`
                        : item.requirement_description}
                    </div>
                  </TableCell>
                  <TableCell className='py-2'>
                    <Badge variant={getStatusVariant(item.status)} className='text-xs'>
                      {getStatusIcon(item.status)}
                      <span className='ml-1'>{getStatusDisplayName(item.status)}</span>
                    </Badge>
                  </TableCell>
                  <TableCell className='py-2'>
                    <div className='flex items-center space-x-2'>
                      <span className='text-xs text-muted-foreground'>
                        {new Date(item.last_evaluated).toLocaleDateString()}
                      </span>
                      <AuditButton
                        requirementId={item.control_id}
                        description={item.requirement_description}
                        onAuditComplete={(result) => handleAuditComplete(item.control_id, result)}
                        size='sm'
                        variant='outline'
                      />
                    </div>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className='border-t pt-2'>
          <div className='flex items-center justify-between'>
            <div className='text-xs text-muted-foreground'>
              Showing {startIndex + 1} to{' '}
              {Math.min(endIndex, filteredData.length)} of {filteredData.length}{' '}
              results
            </div>
            <div className='flex items-center space-x-1'>
              <Button
                variant='outline'
                size='sm'
                onClick={() => goToPage(currentPage - 1)}
                disabled={currentPage === 1}
                className='h-7 w-7 p-0'
              >
                <ChevronLeft size={14} />
              </Button>
              <div className='flex space-x-1'>
                {getPaginationPages().map((page, index) =>
                  page === -1 ? (
                    <span
                      key={`ellipsis-${index}`}
                      className='px-2 py-1 text-muted-foreground text-xs'
                    >
                      ...
                    </span>
                  ) : (
                    <Button
                      key={page}
                      variant={currentPage === page ? 'default' : 'outline'}
                      size='sm'
                      onClick={() => goToPage(page)}
                      className='h-7 w-7 p-0 text-xs'
                    >
                      {page}
                    </Button>
                  )
                )}
              </div>
              <Button
                variant='outline'
                size='sm'
                onClick={() => goToPage(currentPage + 1)}
                disabled={currentPage === totalPages}
                className='h-7 w-7 p-0'
              >
                <ChevronRight size={14} />
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default EvidenceTracker