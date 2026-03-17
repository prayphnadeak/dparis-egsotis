import asyncio
import aiohttp
import time

async def fetch(session, url, i):
    start_time = time.time()
    try:
        async with session.get(url) as response:
            status = response.status
            text = await response.text()
            end_time = time.time()
            print(f"Request {i:02d}: {status} - {end_time - start_time:.3f}s")
            return status, end_time - start_time
    except Exception as e:
        end_time = time.time()
        print(f"Request {i:02d}: FAILED {e} - {end_time - start_time:.3f}s")
        return None, end_time - start_time

async def main():
    url = "http://127.0.0.1:8001/api/v1/tourism/"
    
    print(f"Starting 35 concurrent requests to {url}...")
    
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, i+1) for i in range(35)]
        results = await asyncio.gather(*tasks)
        
    total_time = time.time() - start_time
    print(f"\nCompleted in {total_time:.3f}s")
    
    status_counts = {}
    for r in results:
        status = r[0]
        status_counts[status] = status_counts.get(status, 0) + 1
        
    print(f"\nStatus code summary:")
    for status, count in status_counts.items():
        print(f"HTTP {status}: {count} requests")
        
    if status_counts.get(200, 0) == 30 and status_counts.get(429, 0) == 5:
        print("\nSUCCESS: Rate limiting allows exactly 30 requests and returns 429 for the 5 excess requests.")
    else:
        print("\nFAILED: Expected 30 HTTP 200s and 5 HTTP 429s.")

if __name__ == "__main__":
    asyncio.run(main())
