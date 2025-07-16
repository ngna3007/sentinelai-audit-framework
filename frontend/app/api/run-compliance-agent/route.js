// app/api/run-compliance-agent/route.js
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function POST(request) {
  console.log('🔍 PCI DSS Compliance Audit API Called');
  
  try {
    const body = await request.json();
    console.log('📋 Request body:', body);
    
    // FIXED: Get requirement_id from the frontend (like "1.2.5")
    const requirement_id = body.requirement_id;
    const aws_account_id = body.aws_account_id || 'aws-account-001';
    
    if (!requirement_id) {
      return Response.json({ 
        success: false, 
        message: 'Missing required parameter: requirement_id' 
      }, { status: 400 });
    }

    // Execute Python script with requirement_id
    const command = `cd "/Users/leviron/Project/VPBank Hackathon 2025/sentinelai-audit-framework/my_compliance_agent" && python main.py ${requirement_id} --aws-account ${aws_account_id}`;
    
    console.log('🔧 Executing:', command);

    try {
      const { stdout, stderr } = await execAsync(command, {
        timeout: 300000,
        maxBuffer: 2048 * 1024,
      });

      console.log('✅ Python completed successfully');
      console.log('📝 Output:', stdout);
      if (stderr) console.log('⚠️ Stderr:', stderr);

      // If execAsync doesn't throw, the exit code was 0 (success)
      return Response.json({
        success: true,
        message: `Audit completed successfully for ${requirement_id}`,
        requirement_id: requirement_id,
        output: stdout.trim()
      });

    } catch (error) {
      // execAsync throws if exit code is non-zero (failure)
      console.log('❌ Python script failed');
      console.log('📝 Output:', error.stdout || '');
      console.log('🚨 Error output:', error.stderr || '');
      
      return Response.json({
        success: false,
        message: `Audit failed for ${requirement_id}`,
        requirement_id: requirement_id,
        output: error.stdout || '',
        error_output: error.stderr || '',
        exit_code: error.code || 1
      });
    }

  } catch (error) {
    console.error('❌ API execution failed:', error);
    
    return Response.json({
      success: false,
      message: 'API execution failed',
      error: error.message
    }, { status: 500 });
  }
}

export async function GET() {
  return Response.json({ message: 'Use POST method' }, { status: 405 });
}