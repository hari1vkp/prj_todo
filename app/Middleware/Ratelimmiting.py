import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request,HTTPException

class ratelimit[BaseHTTPMiddleware]:
    def ___init__(self,app,maxreq:int=50,sec:int=60):
        super().__init__(app)
        self.maxreq=maxreq
        self.sec=sec
        self.request=defaultdict(list)
    async def dispatch(self,req:Request,callnext):
        client_ip=req.client.host
        now=time.time()

        self.request[client_ip]= [t for t in self.request[client_ip]
                                    if now-t <self.sec]
        if len(self.request[client_ip])>=self.maxreq:
            raise HTTPException(status_code=429,detail="too many request")
        self.request[client_ip].append(now)
        return await callnext(req)
        