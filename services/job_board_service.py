"""
Job Board Integration Service
Integrates with LinkedIn, Indeed, and other job boards to fetch job descriptions
"""
import requests
from typing import Dict, List, Optional, Any
import re
from urllib.parse import urljoin, urlparse
import time

class JobBoardService:
    """Service for integrating with job boards to fetch job descriptions"""
    
    def __init__(self):
        self.supported_domains = [
            'linkedin.com',
            'indeed.com',
            'glassdoor.com',
            'monster.com',
            'ziprecruiter.com'
        ]
        
        # Rate limiting
        self.last_request_time = {}
        self.min_request_interval = 2  # seconds between requests
        
    def extract_job_from_url(self, url: str) -> Dict[str, Any]:
        """Extract job description from a job board URL"""
        try:
            domain = self._get_domain_from_url(url)
            
            if not self._is_supported_domain(domain):
                return {
                    'error': f'Unsupported job board: {domain}',
                    'supported_domains': self.supported_domains
                }
            
            # Rate limiting
            self._wait_for_rate_limit(domain)
            
            # Extract job based on domain
            if 'linkedin.com' in domain:
                return self._extract_linkedin_job(url)
            elif 'indeed.com' in domain:
                return self._extract_indeed_job(url)
            elif 'glassdoor.com' in domain:
                return self._extract_glassdoor_job(url)
            else:
                return self._extract_generic_job(url)
                
        except Exception as e:
            return {'error': f'Failed to extract job: {str(e)}'}
    
    def search_jobs(self, query: str, location: str = '', job_board: str = 'indeed') -> List[Dict[str, Any]]:
        """Search for jobs on specified job board"""
        try:
            if job_board == 'indeed':
                return self._search_indeed_jobs(query, location)
            elif job_board == 'linkedin':
                return self._search_linkedin_jobs(query, location)
            else:
                return {'error': f'Job search not supported for {job_board}'}
                
        except Exception as e:
            return {'error': f'Job search failed: {str(e)}'}
    
    def _get_domain_from_url(self, url: str) -> str:
        """Extract domain from URL"""
        parsed = urlparse(url)
        return parsed.netloc.lower()
    
    def _is_supported_domain(self, domain: str) -> bool:
        """Check if domain is supported"""
        return any(supported in domain for supported in self.supported_domains)
    
    def _wait_for_rate_limit(self, domain: str):
        """Implement rate limiting"""
        current_time = time.time()
        last_time = self.last_request_time.get(domain, 0)
        
        if current_time - last_time < self.min_request_interval:
            time.sleep(self.min_request_interval - (current_time - last_time))
        
        self.last_request_time[domain] = time.time()
    
    def _extract_linkedin_job(self, url: str) -> Dict[str, Any]:
        """Extract job description from LinkedIn"""
        # Note: LinkedIn has anti-scraping measures, this is a simplified implementation
        # In production, you'd want to use LinkedIn's official API
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML content (simplified)
            content = response.text
            
            # Extract job title
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else 'Job Title Not Found'
            
            # Extract company
            company_match = re.search(r'"companyName":"([^"]+)"', content)
            company = company_match.group(1) if company_match else 'Company Not Found'
            
            # Extract location
            location_match = re.search(r'"locationName":"([^"]+)"', content)
            location = location_match.group(1) if location_match else 'Location Not Found'
            
            # Extract job description (simplified - would need more sophisticated parsing)
            # This is a placeholder implementation
            job_description = "LinkedIn job description extraction requires API access or more sophisticated scraping."
            
            return {
                'success': True,
                'source': 'LinkedIn',
                'title': self._clean_text(title),
                'company': self._clean_text(company),
                'location': self._clean_text(location),
                'description': job_description,
                'url': url,
                'extracted_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except requests.RequestException as e:
            return {
                'error': f'Failed to fetch LinkedIn job: {str(e)}',
                'message': 'LinkedIn requires special handling. Consider copying the job description manually.'
            }
    
    def _extract_indeed_job(self, url: str) -> Dict[str, Any]:
        """Extract job description from Indeed"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            content = response.text
            
            # Extract job title
            title_match = re.search(r'<h1[^>]*class="[^"]*jobsearch-JobInfoHeader-title[^"]*"[^>]*>([^<]+)</h1>', content, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else 'Job Title Not Found'
            
            # Extract company
            company_match = re.search(r'<span[^>]*class="[^"]*companyName[^"]*"[^>]*>([^<]+)</span>', content, re.IGNORECASE)
            company = company_match.group(1).strip() if company_match else 'Company Not Found'
            
            # Extract location
            location_match = re.search(r'<div[^>]*class="[^"]*jobsearch-JobInfoHeader-subtitle[^"]*"[^>]*>.*?<div[^>]*>([^<]+)</div>', content, re.IGNORECASE | re.DOTALL)
            location = location_match.group(1).strip() if location_match else 'Location Not Found'
            
            # Extract job description
            desc_match = re.search(r'<div[^>]*class="[^"]*jobsearch-jobDescriptionText[^"]*"[^>]*>(.*?)</div>', content, re.IGNORECASE | re.DOTALL)
            description = desc_match.group(1) if desc_match else 'Description not found'
            
            # Clean HTML from description
            description = re.sub(r'<[^>]+>', '', description)
            description = re.sub(r'\s+', ' ', description).strip()
            
            return {
                'success': True,
                'source': 'Indeed',
                'title': self._clean_text(title),
                'company': self._clean_text(company),
                'location': self._clean_text(location),
                'description': self._clean_text(description),
                'url': url,
                'extracted_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except requests.RequestException as e:
            return {
                'error': f'Failed to fetch Indeed job: {str(e)}',
                'message': 'Please check the URL or try copying the job description manually.'
            }
    
    def _extract_glassdoor_job(self, url: str) -> Dict[str, Any]:
        """Extract job description from Glassdoor"""
        # Similar implementation to Indeed but with Glassdoor-specific selectors
        return {
            'success': False,
            'error': 'Glassdoor extraction not fully implemented',
            'message': 'Please copy the job description manually for now.'
        }
    
    def _extract_generic_job(self, url: str) -> Dict[str, Any]:
        """Generic job extraction for other sites"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            content = response.text
            
            # Extract title from page title
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else 'Job Title Not Found'
            
            # Try to extract main content
            # Look for common job description containers
            desc_patterns = [
                r'<div[^>]*class="[^"]*job.*?description[^"]*"[^>]*>(.*?)</div>',
                r'<div[^>]*class="[^"]*description[^"]*"[^>]*>(.*?)</div>',
                r'<section[^>]*class="[^"]*job[^"]*"[^>]*>(.*?)</section>'
            ]
            
            description = ''
            for pattern in desc_patterns:
                match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
                if match:
                    description = match.group(1)
                    break
            
            if not description:
                # Fallback: extract text from body
                body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.IGNORECASE | re.DOTALL)
                if body_match:
                    description = body_match.group(1)[:2000]  # Limit to first 2000 chars
            
            # Clean HTML
            description = re.sub(r'<[^>]+>', '', description)
            description = re.sub(r'\s+', ' ', description).strip()
            
            return {
                'success': True,
                'source': 'Generic',
                'title': self._clean_text(title),
                'company': 'Unknown',
                'location': 'Unknown',
                'description': self._clean_text(description)[:3000],  # Limit description length
                'url': url,
                'extracted_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'note': 'Extracted using generic method. Accuracy may vary.'
            }
            
        except requests.RequestException as e:
            return {
                'error': f'Failed to extract job: {str(e)}',
                'message': 'Please copy the job description manually.'
            }
    
    def _search_indeed_jobs(self, query: str, location: str = '') -> List[Dict[str, Any]]:
        """Search for jobs on Indeed (simplified implementation)"""
        # This is a placeholder implementation
        # In production, you'd want to use Indeed's API or more sophisticated scraping
        return {
            'message': 'Job search functionality requires Indeed API access',
            'suggestion': 'Please visit Indeed.com and copy job URLs manually'
        }
    
    def _search_linkedin_jobs(self, query: str, location: str = '') -> List[Dict[str, Any]]:
        """Search for jobs on LinkedIn (simplified implementation)"""
        # This is a placeholder implementation
        # In production, you'd want to use LinkedIn's API
        return {
            'message': 'Job search functionality requires LinkedIn API access',
            'suggestion': 'Please visit LinkedIn.com and copy job URLs manually'
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ''
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove HTML entities
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        
        return text.strip()
    
    def get_supported_domains(self) -> List[str]:
        """Get list of supported job board domains"""
        return self.supported_domains.copy()
    
    def validate_job_url(self, url: str) -> Dict[str, Any]:
        """Validate if a URL is from a supported job board"""
        try:
            domain = self._get_domain_from_url(url)
            is_supported = self._is_supported_domain(domain)
            
            return {
                'valid': is_supported,
                'domain': domain,
                'supported': is_supported,
                'message': 'Supported job board URL' if is_supported else f'Unsupported domain: {domain}'
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'message': 'Invalid URL format'
            }