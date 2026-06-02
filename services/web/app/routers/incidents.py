from fastapi import APIRouter, HTTPException
import os
import logging
import time

router = APIRouter()
logger = logging.getLogger("aidas")

@router.post("/incident/{incident_code}")
def trigger_incident(incident_code: str):
    logger.error(f"[FATAL] 장애 강제 주입 시작: {incident_code}")
    
    try:
        if incident_code == "disk-full":
            with open("/tmp/dummy_disk_fill", "wb") as f:
                f.write(os.urandom(500 * 1024 * 1024))
            return {"message": "Disk Full 장애 주입 완료!"}
        
        elif incident_code == "oom":
            mem_bomb = ["o" * 1024 * 1024 for _ in range(2000)]
            return {"message": "OOM 장애 주입 완료!"}
        
        elif incident_code == "http500":
            # 실제 에러 로그를 남기고 500 에러 응답을 던집니다.
            logger.error("[ERROR] 서버 내부 강제 에러 발생!")
            raise HTTPException(status_code=500, detail="HTTP 500 장애 유발 성공!")
            
        elif incident_code == "db-timeout":
            time.sleep(15)  # 15초 동안 멈춰서 응답 지연 유발
            logger.error("[ERROR] 504: DB Connection Timeout 유발 완료")
            raise HTTPException(status_code=504, detail="DB Connection Timeout 유발 성공!")
            
        else:
            raise HTTPException(status_code=404, detail="알 수 없는 장애 코드입니다.")

    # 💡 여기서 HTTPException을 먼저 잡아주면 504 에러가 500으로 덮어씌워지는 것을 막습니다!
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"[ERROR] 장애 처리 중 예상치 못한 예외 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))