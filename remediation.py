# Name: Python Remediation Script Close Port 22
# Description: This script closes port 22 on an EC2 instance if it is manuallyopened to the world.
# Author: Rob Satnarain
#
# Date Updated   Version      Updated By         Description
# -----------   -----------   ---------------    --------------------------------------
# 2026-04-23    1.0           Rob Satnarain      Initial creation
#
import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Extract details from the EventBridge payload
    detail = event.get('detail', {})
    request_params = detail.get('requestParameters', {})
    
    sg_id = request_params.get('groupId')
    ip_permissions = request_params.get('ipPermissions', {}).get('items', [])
    
    if not sg_id or not ip_permissions:
        logger.info("No relevant Security Group parameters found.")
        return
        
    for permission in ip_permissions:
        from_port = permission.get('fromPort')
        to_port = permission.get('toPort')
        ip_ranges = permission.get('ipRanges', {}).get('items', [])
        
        for ip_range in ip_ranges:
            cidr_ip = ip_range.get('cidrIp')
            
            # The Violation Condition: Port 22 open to the world
            if cidr_ip == '0.0.0.0/0' and from_port == 22:
                logger.info(f"VIOLATION DETECTED: Port 22 open to 0.0.0.0/0 on SG {sg_id}. Reverting...")
                
                try:
                    ec2.revoke_security_group_ingress(
                        GroupId=sg_id,
                        IpPermissions=[permission]
                    )
                    logger.info(f"Successfully revoked unauthorized rule from {sg_id}")
                except Exception as e:
                    logger.error(f"Error revoking rule: {e}")
                    
    return {"status": "Remediation scan complete"}