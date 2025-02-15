import uuid
import base64
import codecs

# 초대코드 생성 함수
def inv_code(length=12):
    """
    generates random code of given length
    """
    return base64.urlsafe_b64encode(
        codecs.encode(uuid.uuid4().bytes, "base64").rstrip()
    ).decode()[:length]

def insert_inv_code(con, cursor):
    # 초대코드 생성
    code = inv_code()
    
    # 새로운 초대코드를 데이터베이스에 추가하는 코드
    cursor.execute(f"""
                   INSERT INTO INVITATION_CODE (CODE, REMAIN_COUNT)
                   VALUES (?, ?);
                   """, (f"{code}", 5))
    con.commit()

# 초대코드 테이블에서 특정 초대코드가 있는지 확인하는 함수입니다.
def inv_code_checker(cursor, inv_code):
    cursor.execute(
        """
        SELECT * FROM INVITATION_CODE
        WHERE CODE = ?;
        """, (inv_code,)
    )
    
    result = cursor.fetchone()
    
    return result

# 
def ticket_office(con, cursor, inv_code):
    # inv_code가 db 내에 있는지 확인
    print_state = True
    result = inv_code_checker(cursor, inv_code)

    if bool(result):
        # db 내에 존재할 경우 현재 남은 사용량 확인
        cnt_usage = int(result[1])
        
        if cnt_usage > 0:
            # 이용 횟수를 하나 차감
            new_cnt_usage = cnt_usage - 1
            cursor.execute(
                """
                UPDATE INVITATION_CODE
                SET REMAIN_COUNT = ?
                WHERE CODE = ?;
                """, (new_cnt_usage, inv_code)
            )
            con.commit()
            
            # 차감 후 남은 사용량 체크
            result = inv_code_checker(cursor, inv_code)
            cnt_usage = int(result[1])
            
            # 남은 사용량이 없을경우 db에서 해당 데이터 삭제
            if cnt_usage == 0:
                cursor.execute(
                    f"""
                    DELETE FROM INVITATION_CODE
                    WHERE CODE = ?;
                    """,
                    (inv_code,)
                )
                con.commit()
            
            authority_state = True
            alert = f"남은 무료이용권은 {cnt_usage}개 입니다.<br>초대코드 - {inv_code}"
            
            return authority_state, print_state, alert
    else:
        authority_state = False
        alert = f"해당 초대코드는 없거나 사용 횟수를 초과했습니다.<br>다른 초대코드를 입력해주세요.<br>초대코드 - {inv_code}"
        
        return authority_state, print_state, alert
