import requests
import json
import time
from datetime import datetime

class CodeGuardAIAgent:
    def __init__(self, api_url):
        self.api_url = api_url
        self.scan_history = []
        
    def display_banner(self):
        banner = """
        🔒 CODEGUARD AI AGENT 🤖
        =========================
        Security Scanner | Built on Android
        =========================
        """
        print(banner)
    
    def get_sample_commits(self):
        return [
            {
                "id": "commit_001",
                "author": "developer@company.com",
                "message": "Add AWS integration",
                "filename": "aws_config.py",
                "code": '''
# AWS Configuration
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
                
def connect_s3():
    return boto3.client("s3")
                ''',
                "risk": "CRITICAL"
            },
            {
                "id": "commit_002", 
                "author": "frontend@company.com",
                "message": "Update login system",
                "filename": "auth.js",
                "code": '''
// Authentication setup
const config = {
    api_key: "sk_live_1234567890abcdef",
    password: "admin123",
    database_url: "mongodb://localhost:27017"
};
                ''',
                "risk": "HIGH"
            },
            {
                "id": "commit_003",
                "author": "devops@company.com", 
                "message": "Clean configuration",
                "filename": "config.py",
                "code": '''
# Safe configuration
DEBUG = True
HOST = "localhost"
PORT = 8000
                
def get_settings():
    return {"env": "development"}
                ''',
                "risk": "LOW"
            }
        ]
    
    def scan_single_commit(self, commit):
        print(f"🔍 Scanning: {commit['filename']}")
        print(f"   Author: {commit['author']}")
        
        try:
            response = requests.post(
                f"{self.api_url}/scan",
                json={
                    "code": commit["code"],
                    "filename": commit["filename"]
                },
                timeout=15
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Connection failed: {str(e)}"}
    
    def execute_security_actions(self, scan_result, commit):
        actions_taken = []
        
        if scan_result.get('action_required'):
            if scan_result['risk_level'] == 'CRITICAL':
                actions_taken.extend([
                    "🚨 CRITICAL: COMMIT BLOCKED AND REVERTED",
                    "📧 Alert sent to security-team@company.com",
                    "🔐 Credentials rotation initiated",
                    "👤 Developer notified: " + commit['author']
                ])
            elif scan_result['risk_level'] == 'HIGH':
                actions_taken.extend([
                    "⚠️ HIGH RISK: COMMIT BLOCKED",
                    "📝 Security review required",
                    "🛡️ Incident ticket #SEC-" + str(hash(commit['id']) % 1000)
                ])
            else:
                actions_taken.extend([
                    "🔸 Security warning issued",
                    "📋 Manual review recommended"
                ])
        else:
            actions_taken.append("✅ Commit approved - No secrets detected")
        
        return actions_taken
    
    def generate_security_report(self):
        total_scans = len(self.scan_history)
        total_findings = sum(entry['findings_count'] for entry in self.scan_history)
        blocked_commits = sum(1 for entry in self.scan_history if entry['findings_count'] > 0)
        
        print("\n" + "="*60)
        print("📊 CODEGUARD AI - SECURITY INTELLIGENCE REPORT")
        print("="*60)
        print(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Commits Scanned: {total_scans}")
        print(f"Security Findings: {total_findings}")
        print(f"Commits Blocked: {blocked_commits}")
        print(f"Risk Prevention: {'EXTREME' if blocked_commits > 0 else 'EXCELLENT'}")
        
        severity_counts = {}
        for entry in self.scan_history:
            for finding in entry.get('findings', []):
                sev = finding['severity']
                severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        if severity_counts:
            print("\n🔍 Findings by Severity:")
            for severity, count in severity_counts.items():
                print(f"   {severity}: {count} findings")
        
        print("="*60)
        
        report_data = {
            "report_id": f"sec_report_{int(time.time())}",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_scans": total_scans,
                "total_findings": total_findings,
                "blocked_commits": blocked_commits
            },
            "detailed_scans": self.scan_history
        }
        
        with open("security_intelligence_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print("💾 Full report saved: security_intelligence_report.json")
    
    def run_complete_workflow(self):
        self.display_banner()
        
        print("🚀 Starting Security Scan Workflow...\n")
        time.sleep(1)
        
        commits = self.get_sample_commits()
        
        print(f"📁 Processing {len(commits)} commits for security analysis...\n")
        
        for i, commit in enumerate(commits, 1):
            print(f"🔄 Processing commit {i}/{len(commits)}")
            print("-" * 40)
            
            scan_result = self.scan_single_commit(commit)
            
            if "error" in scan_result:
                print(f"   ❌ Scan failed: {scan_result['error']}")
                continue
            
            findings_count = scan_result.get('findings_count', 0)
            risk_level = scan_result.get('risk_level', 'UNKNOWN')
            
            print(f"   📈 Findings: {findings_count} | Risk: {risk_level}")
            
            actions = self.execute_security_actions(scan_result, commit)
            for action in actions:
                print(f"   → {action}")
            
            self.scan_history.append({
                "commit_id": commit["id"],
                "author": commit["author"],
                "filename": commit["filename"],
                "timestamp": datetime.now().isoformat(),
                "findings_count": findings_count,
                "risk_level": risk_level,
                "actions_taken": actions,
                "findings": scan_result.get('findings', [])
            })
            
            print()
            time.sleep(1)
        
        self.generate_security_report()
        
        print("\n🎯 CodeGuard AI Agent workflow completed successfully!")
        print("   Your codebase is now more secure! 🔒")

# 🚀 START THE AGENT
if __name__ == "__main__":
    # ⚠️ USE YOUR EXACT URL BELOW ⚠️
    YOUR_REPLIT_URL = "https://d52a813f-bee6-49a2-b031-2ae96bf1dc61-00-1hiymxyt1m0q6.spock.replit.dev"
    
    agent = CodeGuardAIAgent(YOUR_REPLIT_URL)
    agent.run_complete_workflow()
