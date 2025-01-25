from fastapi import HTTPException

from app.utils.logger import make_logger

""" 에러 파싱 모듈 및 HTTPException 정의
    * 클라이언트 표준
        200: Success
        201: Created
        302: Redirected

    * 클라이언트 에러
        400: Bad Request
        401: Unauthorized
        402: Payment Required
        403: Forbidden
        404: Not Found
        409: Conflict
        422: 클라이언트 전송 데이터와 백앤드 스키마 불일치
        452: exceed_request, 클라이언트 요청 횟수 초과
        453: invalid_verification_request,
        454: invalid_verification_already_done,
        455: invalid_verification_not_found,
        456: invalid_authentication_request,
        457: invalid_authorization_request,
        458: invalid_user_session_request,
        459: invalid_user_session_expired,
        460: invalid_paid_user_expired,
        461: invalid_paid_user_not_enough_pricing_tier,
        480: data_integrity
        499: Max Client Error Code
        500: Internal Server Error
        512: 메일 전송 오류
        599: Max Server Error Code

    * 사용자 정의 에러 메시지
        801: 사용자 세션이 없음
        802: useStore에서 사용자 정보를 가져올 수 없음.

    * 프론트 엔드 에러
        0: Init Code
        999: Max Error Code
"""

logger = make_logger(__name__)


class BaseException(HTTPException):
    def __init__(self, status_code=500, detail="Internal Server Error"):
        self.status_code = status_code
        self.detail = detail
        logger.error(detail)


class Exception400(BaseException):
    def __init__(self, type="base", detail=""):
        self.msgs = {
            "base": "Bad Request",
            "RepeatIsNotVaild": "Repeat must have value like -1 or 1,2,3...",
        }
        super().__init__(status_code=400, detail=self.msgs[type] + detail)


class Exception403(BaseException):
    def __init__(self, type="base", detail=""):
        self.msgs = {"base": "Forbidden"}
        super().__init__(status_code=403, detail=self.msgs[type] + detail)


class Exception404(BaseException):
    def __init__(self, type="base", detail=""):
        self.msgs = {
            "base": "Not Found",
            "ClientDoesNotExists": "Client not exists in socket. Please check your socket connection.",
            "PresetDoesNotExists": "Preset doesn't exists. Please check id.",
            "ConnectionDoesNotExists": "Connection doesn't exists. Please check id.",
            "MotorEquipmentDoesNotExists": "Equipment doesn't exists. Please check motor metadata.",
            "MotorSettingsDoesNotExists": "MotorSettings doesn't exists. Please check motor_settings_id.",
            "WaveformDoesNotExists": "WaveForms doesn't exists. Please check your preset.",
        }
        super().__init__(status_code=404, detail=self.msgs[type] + detail)


class Exception409(BaseException):
    def __init__(self, type="base", detail=""):
        self.msgs = {
            "base": "Confilict",
            "MotorSettingsAlreadyExists": "MotorSettings already exists. Please check your data.",
            "PresetAlreadyExists": "Preset already exists. Please check your data.",
            "WaveformAlreadyExists": "Waveform already exists. Please check your data.",
        }
        super().__init__(status_code=409, detail=self.msgs[type] + detail)


class Exception500(BaseException):
    def __init__(self, type="base", detail=""):
        self.msgs = {
            "base": "Internal Server Error",
            "MqConnectionFailed": "Failed to connect mq. Please check your config.",
            "FailedToDeletePreset": "Failed to delete preset. Please check your preset_id.",
        }
        super().__init__(status_code=500, detail=self.msgs[type] + detail)
