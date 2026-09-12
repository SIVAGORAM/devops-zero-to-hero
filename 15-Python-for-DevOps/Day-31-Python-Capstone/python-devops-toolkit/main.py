import argparse
from dotenv import load_dotenv
from devops.system import get_system_info
from devops.api import health_check
from devops.logger import setup_logger
from devops.files import create_backup
from devops.aws import get_ec2_instances

load_dotenv()
logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description='DevOps Toolkit')
    subparsers = parser.add_subparsers(dest='command')
    
    subparsers.add_parser('system')
    
    health_parser = subparsers.add_parser('health')
    health_parser.add_argument('--url', required=True)
    
    subparsers.add_parser('backup')
    subparsers.add_parser('aws')
    subparsers.add_parser('deploy')
    
    args = parser.parse_args()
    
    if args.command == 'system':
        for k, v in get_system_info().items(): print(f'{k}: {v}')
    elif args.command == 'health':
        print(health_check(args.url))
    elif args.command == 'backup':
        if create_backup('config', 'backups'): print('Backup complete')
    elif args.command == 'aws':
        try:
            for i in get_ec2_instances('ap-south-1'): print(i)
        except Exception as e: print(f'AWS Error: {e}')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
