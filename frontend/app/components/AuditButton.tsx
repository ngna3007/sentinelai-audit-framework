// components/AuditButton.tsx
"use client";
import React, { useState } from 'react';
import { Bot, Loader, CheckCircle, XCircle, Clock, AlertCircle } from 'lucide-react';

interface AuditButtonProps {
  requirementId: string; // This is the control_id like "1.2.5" 
  description: string;
  onAuditComplete?: (result: any) => void;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'primary' | 'secondary' | 'outline';
}

interface AuditResult {
  success: boolean;
  message: string;
  compliance_status?: 'In Place' | 'Not In Place' | 'Not Applicable' | 'Pending' | 'compliant' | 'non_compliant' | 'not_applicable' | 'pending';
  findings?: string;
  recommendations?: string;
  risk_level?: string;
  evidence_url?: string;
  raw_output?: string;
  error?: string;
}

const AuditButton: React.FC<AuditButtonProps> = ({
  requirementId,
  description,
  onAuditComplete,
  size = 'sm',
  variant = 'primary'
}) => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AuditResult | null>(null);
  const [showDetails, setShowDetails] = useState(false);

// In AuditButton.tsx, update the runAudit function:

const runAudit = async () => {
  setLoading(true);
  setResult(null);
  setShowDetails(false);
  
  try {
    console.log('🤖 Starting PCI DSS audit for requirement:', requirementId);
    console.log('Sending audit request:', {
      requirement_id: requirementId,  // FIXED: Use requirement_id instead of operation
      description: description.substring(0, 100) // Truncate for logging
    });

    const response = await fetch('/api/run-compliance-agent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        requirement_id: requirementId,  // FIXED: Send requirement_id (like "1.2.5")
        // aws_account_id will be added by the backend from context if needed
        description: description
      })
    });
    
    console.log('Audit API response status:', response.status);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('Audit API error response:', errorText);
      throw new Error(`HTTP ${response.status}: ${errorText}`);
    }
    
    const data = await response.json();
    console.log('Audit result received:', {
      success: data.success,
      message: data.message,
      requirement_id: data.requirement_id
    });
    
    setResult(data);
    
    // Callback to parent component with result
    if (onAuditComplete) {
      onAuditComplete(data);
    }
    
    // Auto-show details if there's an error
    if (!data.success || data.error) {
      setShowDetails(true);
    }
  } catch (error: any) {
    console.error('Audit execution failed:', error);
    const errorResult = { 
      success: false, 
      message: 'Failed to execute PCI DSS audit',
      error: error.message,
      findings: 'Audit system error occurred',
      recommendations: 'Please check system configuration and try again'
    };
    setResult(errorResult);
    setShowDetails(true);
    
    if (onAuditComplete) {
      onAuditComplete(errorResult);
    }
  } finally {
    setLoading(false);
  }
};

  const getSizeClasses = () => {
    switch (size) {
      case 'sm':
        return 'px-2 py-1 text-xs';
      case 'md':
        return 'px-3 py-2 text-sm';
      case 'lg':
        return 'px-4 py-2 text-base';
      default:
        return 'px-2 py-1 text-xs';
    }
  };

  const getVariantClasses = () => {
    switch (variant) {
      case 'primary':
        return 'bg-blue-600 hover:bg-blue-700 text-white border-blue-600';
      case 'secondary':
        return 'bg-gray-600 hover:bg-gray-700 text-white border-gray-600';
      case 'outline':
        return 'bg-white hover:bg-gray-50 text-gray-700 border-gray-300';
      default:
        return 'bg-blue-600 hover:bg-blue-700 text-white border-blue-600';
    }
  };

  const getStatusColor = (status: string) => {
    const normalizedStatus = status.toLowerCase().replace(/\s+/g, '_');
    switch (normalizedStatus) {
      case 'in_place':
      case 'compliant':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'not_in_place':
      case 'non_compliant':
      case 'non-compliant':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'not_applicable':
      case 'not_applicable':
        return 'text-gray-600 bg-gray-50 border-gray-200';
      case 'pending':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      default:
        return 'text-blue-600 bg-blue-50 border-blue-200';
    }
  };

  const getStatusIcon = (status: string) => {
    const normalizedStatus = status.toLowerCase().replace(/\s+/g, '_');
    switch (normalizedStatus) {
      case 'in_place':
      case 'compliant':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'not_in_place':
      case 'non_compliant':
      case 'non-compliant':
        return <XCircle className="w-4 h-4 text-red-600" />;
      case 'not_applicable':
        return <AlertCircle className="w-4 h-4 text-gray-600" />;
      case 'pending':
        return <Clock className="w-4 h-4 text-yellow-600" />;
      default:
        return <Clock className="w-4 h-4 text-blue-600" />;
    }
  };

  const getRiskLevelColor = (riskLevel: string) => {
    switch (riskLevel?.toLowerCase()) {
      case 'high':
        return 'text-red-600 bg-red-100';
      case 'medium':
        return 'text-yellow-600 bg-yellow-100';
      case 'low':
        return 'text-green-600 bg-green-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="relative">
      {/* Audit Button */}
      <button
        onClick={runAudit}
        disabled={loading}
        className={`
          inline-flex items-center space-x-1 rounded border font-medium
          disabled:opacity-50 disabled:cursor-not-allowed
          transition-colors duration-200
          ${getSizeClasses()}
          ${getVariantClasses()}
        `}
        title={`Run AI audit for PCI DSS requirement ${requirementId}`}
      >
        {loading ? (
          <Loader className="w-3 h-3 animate-spin" />
        ) : (
          <Bot className="w-3 h-3" />
        )}
        <span>
          {loading ? 'Auditing...' : 'AI Audit'}
        </span>
      </button>

      {/* Results Modal/Popup */}
      {result && (
        <div className="absolute z-50 top-full left-0 mt-2 w-96 max-w-screen-sm">
          <div className={`
            border rounded-lg p-4 shadow-lg bg-white max-h-96 overflow-y-auto
            ${result.success ? 'border-blue-200' : 'border-red-200'}
          `}>
            {/* Header */}
            <div className="flex items-center justify-between mb-3">
              <h4 className="font-semibold text-gray-900 flex items-center space-x-2">
                <Bot className="w-4 h-4" />
                <span>PCI DSS Audit Result</span>
              </h4>
              <button
                onClick={() => setResult(null)}
                className="text-gray-400 hover:text-gray-600 text-lg leading-none"
              >
                ✕
              </button>
            </div>

            {/* Requirement Info */}
            <div className="mb-3 p-2 bg-gray-50 rounded border">
              <div className="text-xs font-medium text-gray-600">Requirement {requirementId}</div>
              <div className="text-xs text-gray-500 mt-1">
                {description.length > 100 ? `${description.substring(0, 100)}...` : description}
              </div>
            </div>

            {/* Content */}
            <div className="space-y-3">
              <p className="text-sm text-gray-700">{result.message}</p>
              
              {/* Compliance Status */}
              {result.compliance_status && (
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-medium text-gray-500">Status:</span>
                  <div className={`
                    inline-flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium border
                    ${getStatusColor(result.compliance_status)}
                  `}>
                    {getStatusIcon(result.compliance_status)}
                    <span>{result.compliance_status}</span>
                  </div>
                </div>
              )}

              {/* Risk Level */}
              {result.risk_level && (
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-medium text-gray-500">Risk:</span>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${getRiskLevelColor(result.risk_level)}`}>
                    {result.risk_level}
                  </span>
                </div>
              )}

              {/* Findings */}
              {result.findings && (
                <div>
                  <span className="text-xs font-medium text-gray-500">Findings:</span>
                  <p className="text-xs text-gray-600 mt-1 p-2 bg-gray-50 rounded border">
                    {result.findings}
                  </p>
                </div>
              )}

              {/* Recommendations */}
              {result.recommendations && (
                <div>
                  <span className="text-xs font-medium text-gray-500">Recommendations:</span>
                  <p className="text-xs text-gray-600 mt-1 p-2 bg-blue-50 rounded border border-blue-200">
                    {result.recommendations}
                  </p>
                </div>
              )}

              {/* Evidence URL */}
              {result.evidence_url && (
                <div>
                  <span className="text-xs font-medium text-gray-500">Evidence:</span>
                  <a 
                    href={result.evidence_url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-xs text-blue-600 hover:text-blue-800 underline ml-2"
                  >
                    View Evidence
                  </a>
                </div>
              )}

              {/* Error Details */}
              {result.error && (
                <div>
                  <span className="text-xs font-medium text-red-600">Error:</span>
                  <p className="text-xs text-red-600 mt-1 p-2 bg-red-50 rounded border border-red-200">
                    {result.error}
                  </p>
                </div>
              )}

              {/* Detailed Output */}
              {result.raw_output && (
                <details className="text-xs">
                  <summary className="cursor-pointer text-blue-600 font-medium hover:text-blue-800">
                    View detailed audit output
                  </summary>
                  <pre className="mt-2 bg-gray-50 border rounded p-2 text-xs overflow-auto max-h-32 text-gray-700 whitespace-pre-wrap">
                    {result.raw_output}
                  </pre>
                </details>
              )}

              {/* Actions */}
              <div className="flex items-center justify-between pt-2 border-t">
                <button
                  onClick={() => setShowDetails(!showDetails)}
                  className="text-xs text-blue-600 hover:text-blue-800 font-medium"
                >
                  {showDetails ? 'Hide Details' : 'Show Details'}
                </button>
                <div className="text-xs text-gray-400">
                  Audited at {new Date().toLocaleTimeString()}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AuditButton;