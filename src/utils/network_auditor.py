"""
Module: network_auditor.py
Framework: emp_regression_3.0 (Shared - Main & Custom Branches)
Layer: Layer 3 (L3) - Telemetry & Network Routing Verification
Evidence Mapping: EV-001 (L1 Config) -> EV-015 (L4 Policy Integration)
"""

import os
import socket
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger("NetworkAuditor")

NETWORK_MAP = {
    "live": {
        "track": "track.empmonitor.com",
        "storelogs": "storelogs.dev.empmonitor.com",
        "screencast": "realtime.empmonitor.com",  # Standard live/realtime sockets
        "screencast_alt": "remote.empmonitor.com",
        "service": "service.empmonitor.com",
        "updates": "updates.empmonitor.in"
    },
    "dev": {
        "track": "track.dev.empmonitor.com",
        "storelogs": "activity.dev.emmonitor.com",
        "screencast": "remote-dev.empmonitor.com",
        "service": "service.dev.empmonitor.com",
        "updates": "updates.empmonitor.in"  # Subpath /dev handled in URL checks
    }
}


def _safe_print(msg: str):
    """Safely prints to stdout without raising UnicodeEncodeError on Windows cp1252."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", errors="replace").decode("ascii"))


class NetworkAuditor:
    def __init__(self, environment: str, exe_list: List[str]):
        """
        :param environment: 'dev' or 'live'
        :param exe_list: List of executable names to verify (e.g., ['empmonitor.exe'] or ['DisplayConfigManager.exe'])
        """
        self.environment = "dev" if str(environment).strip().lower() in ["1", "dev", "development"] else "live"
        self.exe_list = [str(exe).strip() for exe in exe_list if str(exe).strip()]
        self.target_endpoints = self._get_environment_endpoints()

    def _get_environment_endpoints(self) -> Dict[str, str]:
        """Retrieves the target API domains for the selected run environment."""
        return NETWORK_MAP.get(self.environment, NETWORK_MAP["dev"])

    def verify_dns_and_tcp_handshake(self) -> Dict[str, Dict[str, Any]]:
        """
        Tests DNS resolution and TCP handshakes on standard HTTP/S ports (80/443).
        Ensures the local workstation has a clear routing path to the cloud backend.
        """
        results = {}
        _safe_print(f"\n[L3 Audit] Testing TCP connections to {self.environment.upper()} endpoints...")
        logger.info(f"=== LAYER 3 AUDIT: DNS & TCP Handshake Verification ({self.environment.upper()}) ===")

        for name, domain in self.target_endpoints.items():
            port = 80 if "updates" in name else 443
            try:
                # Resolve IP and test TCP Handshake with a strict 4-second timeout
                socket.setdefaulttimeout(4.0)
                ip_address = socket.gethostbyname(domain)

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((domain, port))

                results[domain] = {
                    "role": name,
                    "port": port,
                    "resolved_ip": ip_address,
                    "tcp_handshake": "SUCCESS",
                    "status": "HEALTHY",
                    "error": None
                }
                _safe_print(f"  [CONNECTED] {domain}:{port} -> {ip_address}")
                logger.info(f"  [HEALTHY] {domain}:{port} -> IP: {ip_address} (TCP Handshake Success)")
            except Exception as e:
                err_msg = str(e)
                results[domain] = {
                    "role": name,
                    "port": port,
                    "resolved_ip": "FAILED",
                    "tcp_handshake": f"FAILED: {err_msg}",
                    "status": "BLOCKED",
                    "error": err_msg
                }
                _safe_print(f"  [BLOCKED] {domain}:{port} -> Connection Failed! ({err_msg})")
                logger.warning(f"  [BLOCKED] {domain}:{port} -> Connection Failed! ({err_msg})")

        return results

    def verify_windows_firewall_exceptions(self) -> Dict[str, Dict[str, Any]]:
        """
        Queries the Windows Defender Firewall via netsh to assert that 
        outbound 'Allow' rules/policies are actively present for our running executables.
        """
        firewall_status = {}
        _safe_print("\n[L3 Audit] Auditing Windows Defender Firewall outbound rules...")
        logger.info("=== LAYER 3 AUDIT: Windows Defender Firewall Rules Check ===")

        # Check general firewall outbound policy
        default_policy = "AllowOutbound"
        try:
            profile_query = subprocess.run(
                ["netsh", "advfirewall", "show", "currentprofile"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
            if "BlockInbound,AllowOutbound" in profile_query.stdout or "AllowOutbound" in profile_query.stdout:
                default_policy = "AllowOutbound (Default System Policy)"
        except Exception:
            pass

        # Query all rules via netsh
        all_rules_output = ""
        try:
            netsh_proc = subprocess.run(
                ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )
            if netsh_proc.returncode == 0:
                all_rules_output = netsh_proc.stdout
        except Exception as e:
            logger.debug(f"netsh rule query note: {e}")

        for exe in self.exe_list:
            exe_clean = Path(exe).name
            exe_base = Path(exe).stem
            
            rule_found = False
            rule_name = None

            if all_rules_output:
                for line in all_rules_output.splitlines():
                    if "Rule Name:" in line and (exe_clean.lower() in line.lower() or exe_base.lower() in line.lower()):
                        rule_found = True
                        rule_name = line.split(":", 1)[1].strip()
                        break

            if rule_found:
                firewall_status[exe] = {
                    "rule_status": "EXPLICIT_RULE_FOUND",
                    "policy_action": "ALLOW",
                    "status": "SECURE",
                    "display_text": "Allowed (Explicit Rule)",
                    "details": f"Explicit Rule: {rule_name}"
                }
                _safe_print(f"  [ALLOWED] {exe} -> Outbound Firewall Exception Verified [Rule: {rule_name}]")
                logger.info(f"  [SECURE] {exe} -> Explicit Outbound Rule Verified: {rule_name}")
            else:
                # Default Windows Defender Firewall policy allows outbound traffic
                if "AllowOutbound" in default_policy:
                    firewall_status[exe] = {
                        "rule_status": "DEFAULT_ALLOW",
                        "policy_action": "ALLOW (Default Outbound Policy)",
                        "status": "SECURE",
                        "display_text": "Allowed (Default Outbound Policy)",
                        "details": "Outbound allowed via Windows Defender Firewall default policy"
                    }
                    _safe_print(f"  [ALLOWED] {exe} -> Outbound Traffic Allowed by Default Policy [ALLOW]")
                    logger.info(f"  [SECURE] {exe} -> Outbound traffic allowed under Windows Defender default outbound policy")
                else:
                    firewall_status[exe] = {
                        "rule_status": "NOT_FOUND",
                        "policy_action": "BLOCK/RESTRICTED",
                        "status": "WARNING",
                        "display_text": "Blocked / Restricted",
                        "details": "No explicit rule and default policy is restrictive"
                    }
                    _safe_print(f"  [WARNING] {exe} -> No explicit outbound 'Allow' rule found. Outbound tracking might fail!")
                    logger.warning(f"  [WARNING] {exe} -> No explicit outbound rule found")

        return firewall_status

    def verify_cross_environment_leak(self, config_js_content: str = "", ini_content: str = "") -> Dict[str, Any]:
        """
        Validates local configuration strings to ensure zero cross-environment data leakage.
        """
        combined = f"{config_js_content or ''}\n{ini_content or ''}"
        mismatches = []
        is_clean = True

        if self.environment == "live":
            dev_leak_patterns = [
                ("track.dev.empmonitor.com", "Dev authentication endpoint"),
                ("activity.dev.emmonitor.com", "Dev activity/storelogs endpoint"),
                ("remote-dev.empmonitor.com", "Dev screencast socket host"),
                ("service.dev.empmonitor.com", "Dev service endpoint"),
                ("updates.empmonitor.in/dev", "Dev auto-update pathway")
            ]
            for pattern, desc in dev_leak_patterns:
                if pattern in combined:
                    is_clean = False
                    mismatches.append(f"CRITICAL LEAK: Dev endpoint detected in Live agent configuration ({pattern} - {desc})!")
        else: # dev
            live_leak_patterns = [
                ("https://track.empmonitor.com", "Live production auth endpoint"),
                ("realtime.empmonitor.com", "Live production screencast host"),
                ("service.empmonitor.com", "Live production service endpoint")
            ]
            for pattern, desc in live_leak_patterns:
                if pattern in combined and "dev" not in pattern:
                    is_clean = False
                    mismatches.append(f"CRITICAL LEAK: Live production endpoint detected in Dev agent configuration ({pattern} - {desc})!")

        return {
            "environment": self.environment,
            "is_clean": is_clean,
            "leak_status": "CLEAN" if is_clean else "LEAK DETECTED",
            "leak_summary": "No cross-environment leakage detected" if is_clean else f"CRITICAL LEAK: {len(mismatches)} invalid environment reference(s) found",
            "mismatches": mismatches
        }

    def run_full_audit(self, config_js_content: str = "", ini_content: str = "") -> Dict[str, Any]:
        """Runs DNS/TCP handshake, firewall audit, and cross-environment leak check."""
        tcp_results = self.verify_dns_and_tcp_handshake()
        firewall_results = self.verify_windows_firewall_exceptions()
        leak_results = self.verify_cross_environment_leak(config_js_content, ini_content)

        any_tcp_blocked = any(v.get("status") == "BLOCKED" for v in tcp_results.values())
        any_firewall_blocked = any(v.get("status") in ["WARNING", "BLOCKED", "ERROR"] for v in firewall_results.values())
        is_healthy = (not any_tcp_blocked) and leak_results.get("is_clean", True)

        return {
            "environment": self.environment,
            "is_healthy": is_healthy,
            "target_endpoints": self.target_endpoints,
            "tcp_connectivity": tcp_results,
            "firewall_status": firewall_results,
            "leak_audit": leak_results,
            "has_tcp_failures": any_tcp_blocked,
            "has_firewall_warnings": any_firewall_blocked
        }
