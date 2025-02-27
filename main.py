import typer
import os
from rich.console import Console
from pathlib import Path
import shutil
import stat

app = typer.Typer()
console = Console()

GAME_DIR = "space_mystery"
LOCATIONS_DIR = f"{GAME_DIR}/locations"
EVIDENCE_DIR = f"{GAME_DIR}/evidence"
CREW_DIR = f"{GAME_DIR}/crew_logs"
SECURITY_DIR = f"{GAME_DIR}/security"
HIDDEN_DIR = f"{GAME_DIR}/.hidden"

# 장소 정의 (한글 이름)
LOCATIONS = {
    "bridge": "함교",
    "lab": "실험실",
    "medbay": "의무실",
    "engine": "엔진실",
    "quarters1": "선원_숙소_A구역",
    "quarters2": "선원_숙소_B구역",
    "cafeteria": "식당",
    "comms": "통신실",
    "security": "보안실",
    "maintenance": "정비실"
}

# 선원 정의 (한글 이름)
CREW_MEMBERS = [
    "선장_이강욱",
    "엔지니어_조재휘",
    "의사_신종우",
    "보안_김혜성",
    "과학책임자_김르탄",  # 사망자
    "항해사_박지희",
    "통신담당_이진호",
    "정비사_오성택",
    "AI전문가_허원영"
]

def create_game_files():
    # 게임 디렉토리 생성
    for dir_path in [GAME_DIR, EVIDENCE_DIR, CREW_DIR, SECURITY_DIR, HIDDEN_DIR]:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # 장소 디렉토리 생성
    Path(LOCATIONS_DIR).mkdir(parents=True, exist_ok=True)
    for loc_key in LOCATIONS.keys():
        Path(f"{LOCATIONS_DIR}/{loc_key}").mkdir(parents=True, exist_ok=True)

    # 증거 파일들 생성
    with open(f"{EVIDENCE_DIR}/부검_보고서.txt", "w") as f:
        f.write("피해자: 과학책임자 김르탄\n")
        f.write("사망 시간: 2184년 3월 15일 02:30\n")
        f.write("사인: 질식사\n")
        f.write("특이사항: 목 부위에 끈으로 조인 흔적 발견\n")
        f.write("피해자의 손에서 빨간색 섬유 발견\n")
        f.write("피해자의 손톱 밑에서 이상한 녹색 물질 발견 - 분석 중\n")
        f.write("피해자의 체내에서 미량의 진정제 성분 발견\n")

    with open(f"{EVIDENCE_DIR}/범죄현장.txt", "w") as f:
        f.write("발견 장소: 실험실\n")
        f.write("실험실 내부는 정돈되어 있었으며 싸움의 흔적 없음\n")
        f.write("피해자의 컴퓨터는 켜져 있었음\n")
        f.write("* 'ls -la' 명령어로 숨겨진 파일을 확인해보세요 *\n")

    # 선원들의 로그 파일
    crew_logs = {
        "선장_이강욱": "03-14 23:45 - 야간 순찰 완료\n03-15 02:15 - 엔진 이상 보고 받음\n03-15 02:40 - 엔진실 점검\n* 김르탄이 최근 나에게 중요한 보고를 하려 했으나 시간이 없어 미뤘다. 무슨 내용이었을까? *",
        "엔지니어_조재휘": "03-14 23:30 - 엔진 정기 점검\n03-15 02:15 - 엔진 과열 발생, 선장에게 보고\n03-15 02:30 - 엔진 냉각 시스템 작동\n* 김르탄과 최근 연구 자금 배분에 대해 심하게 다툰 적이 있다. 그가 내 프로젝트 예산을 삭감했다. *",
        "의사_신종우": "03-14 23:00 - 의무실 정리\n03-15 02:20 - 김르탄이 실험실에 혼자 있는 것을 봄\n03-15 02:45 - 비명 소리를 들음\n* 이진호의 최근 건강검진에서 이상한 점을 발견했다. 인간의 생체 지표가 아니다. *\n* 진정제 몇 병이 사라졌다. 누가 가져간 걸까? *",
        "보안_김혜성": "03-14 23:50 - 보안 카메라 점검\n03-15 02:00 - 순찰 시작\n03-15 02:35 - 실험실 근처에서 수상한 소리\n* 김르탄이 내 보안 권한으로 접근할 수 없는 파일을 만들었다. 그가 무엇을 숨기고 있는지 조사 중이다. *",
        "과학책임자_김르탄": "03-14 23:00 - 새로운 발견\n03-15 02:00 - 중요한 분석 결과... 누군가 오는 소리가...\n* 우리 중 한 명이 인간이 아니다. 증거를 모았다. 선장에게 즉시 보고해야 한다. *",
        "항해사_박지희": "03-14 23:15 - 항로 재설정\n03-15 02:10 - 휴식 시작\n03-15 02:40 - 이상한 소리에 깨어남\n* 김르탄이 내 항해 기록을 몰래 확인했다. 왜 그랬을까? 내가 엘리스 성운 근처로 항로를 약간 변경한 것을 알게 된 걸까? *",
        "통신담당_이진호": "03-14 23:40 - 통신 장비 점검\n03-15 02:20 - 통신실 작업 완료\n03-15 02:50 - 비상 통신 수신\n* 김르탄이 내 통신 기록을 조사하고 있었다. 그가 무엇을 발견했는지 알아내야 한다. *",
        "정비사_오성택": "03-14 23:20 - 정비실 작업 완료\n03-15 02:15 - 엔진실에서 조재휘와 대화\n03-15 02:30 - 정비실로 복귀\n* 환기구 수리 중 김르탄의 실험실에서 이상한 소리를 들었다. 그가 금지된 실험을 하고 있는 것 같다. *",
        "AI전문가_허원영": "03-14 23:30 - AI 시스템 업데이트\n03-15 02:20 - 시스템 오류 감지\n03-15 02:35 - 실험실 근처에서 이상한 움직임 감지\n* AI 행동 분석 알고리즘이 여러 선원들에게서 이상 패턴을 감지했다. 누가 진짜 문제인지 판단하기 어렵다. *"
    }

    for crew, log in crew_logs.items():
        with open(f"{CREW_DIR}/{crew}_일지.txt", "w") as f:
            f.write(log)

    # 숨겨진 파일들
    with open(f"{HIDDEN_DIR}/.비밀_메시지.txt", "w") as f:
        f.write("이진호의 비밀 통신 내용을 우연히 발견했다.\n")
        f.write("그가 우주선의 기밀 정보를 외부로 유출하고 있다.\n")
        f.write("더 충격적인 것은, 그의 DNA 분석 결과가 인간이 아니라는 점이다.\n")
        f.write("이건 위험한 발견이다. 즉시 선장에게 보고해야...\n")

    # 보안 카메라 영상 (바이너리 파일인 것처럼)
    with open(f"{SECURITY_DIR}/카메라_02_15.bin", "w") as f:
        f.write("02:15 - 조재휘와 오성택이 엔진실에서 대화\n")
        f.write("02:25 - 이진호가 실험실 쪽으로 향함\n")
        f.write("02:30 - 화면 일시적 정전\n")
        f.write("02:35 - 김혜성과 허원영이 복도를 지나감\n")


    # 파일 권한 설정
    os.chmod(f"{CREW_DIR}/통신담당_이진호_일지.txt", stat.S_IRUSR | stat.S_IWUSR)
    os.chmod(f"{HIDDEN_DIR}/.비밀_메시지.txt", stat.S_IRUSR | stat.S_IWUSR)

    # 장소별 물건/증거 배치
    location_items = {
        "bridge": {
            "항해_일지.txt": "항해 일지: 최근 엘리스 성운 근처를 지나감",
            "우주_지도.txt": "우주 지도: 현재 위치와 예정 경로 표시",
            "선장_메모.txt": "선장 메모: 최근 통신 장비 이상에 대한 보고 받음",
            "비상_프로토콜.txt": "비상 프로토콜: 외계 생명체 접촉 시 격리 절차"
        },
        "lab": {
            "연구_데이터.txt": "연구 데이터: 김르탄의 최근 프로젝트 기록",
            "샘플_분석.txt": "샘플 분석: 미확인 녹색 물질 - 지구상에 존재하지 않는 원소 구성",
            "실험_일지.txt": "샘플 데이터가 이상하다... 이것은 엘리스 종족의 특수한 물질이다.",
            "엘리스인_분석.txt": "엘리스인은 지구인보다 낮은 체온을 가지고 있다."
        },
        "medbay": {
            "의료_보고서.txt": "의료 보고서: 모든 선원의 건강 상태. 신종우가 몇몇 기록을 수정한 흔적 있음.",
            "약품_목록.txt": "약품 목록: 최근 수면제와 진정제 일부 분실됨. 신종우만 접근 가능한 캐비닛에서 사라짐.",
            "건강검진_결과.txt": "건강검진 결과: 이진호가 정기 검진을 계속 미룸. 조재휘와 허원영도 최근 검진을 거부함.",
            "의사_노트.txt": "의사 노트: 김르탄이 비밀리에 혈액 샘플을 가져와 분석 요청함. 신종우의 개인 메모에 '김르탄이 너무 많은 것을 알고 있다'라고 적혀 있음."
        },
        "engine": {
            "엔진_상태.txt": "엔진 상태: 정상 작동 중이나 최근 원인 불명의 과열 현상 발생.",
            "정비_기록.txt": "정비 기록: 03-15 02:15 엔진 과열 발생. 조재휘가 빠르게 대응했으나 원인은 불명확.",
            "냉각_시스템.txt": "냉각 시스템: 03-15 02:30 비상 냉각 작동. 시스템 로그에 누군가 수동으로 과열을 유발한 흔적 있음.",
            "에너지_흐름.txt": "에너지 흐름: 02:30경 통신실과 실험실에서 비정상적인 에너지 소비 감지. 누군가 고출력 장비를 작동시킴."
        },
        "quarters1": {
            "침실_배정.txt": "침실 배정: A구역 - 이강욱, 조재휘, 신종우, 김혜성",
            "개인_소지품.txt": "개인 소지품 목록:\n\n이강욱(선장): 가족사진, 오래된 나침반, 지구에서 가져온 위스키 한 병\n\n조재휘(엔지니어): 엔진 설계도, 수리 도구 세트, 로봇 모형 컬렉션\n\n신종우(의사): 의학 서적, 개인 의료 키트, 희귀 약초 표본\n\n김혜성(보안): 보안 매뉴얼, 개인 무기(스턴건), 무술 훈련 장비",
            "당직_표.txt": "당직 표: 03-15 새벽 당직은 김혜성",
            "김르탄_메모.txt": "김르탄의 메모: '누군가 우리 중에 있다. 더 조사해야 한다.'"
        },
        "quarters2": {
            "침실_배정.txt": "침실 배정: B구역 - 김르탄, 박지희, 이진호, 오성택, 허원영",
            "개인_소지품.txt": "개인 소지품 목록:\n\n김르탄(과학책임자): 연구 노트, 첨단 현미경, 지구 식물 표본, 잠긴 금속 케이스\n\n박지희(항해사): 별자리 지도, 개인 항법 장치, 고대 천문학 서적, 엘리스 성운에 관한 비정상적 관심을 보이는 노트\n\n이진호(통신담당): 통신 장비 부품, 개인용 데이터 패드(암호화됨)\n\n오성택(정비사): 맞춤형 공구 세트, 기계 부품 컬렉션, 자동화 로봇 프로토타입, 환기구 접근 코드\n\n허원영(AI전문가): 양자 컴퓨팅 장치, AI 알고리즘 노트, 홀로그램 투영기, 선원들의 행동 패턴 분석 데이터",
            "이진호_서랍.txt": "이진호의 서랍: 이상한 금속 장치 발견. 지구 기술로는 만들어질 수 없는 합금으로 제작됨. 표면에 미세한 회로와 푸른빛 결정체가 박혀 있음. 작동 방식 불명.",
            "일정표.txt": "일정표: 이진호가 자주 야간에 통신실에 있음. 박지희도 정규 근무 시간 외에 함교에 자주 출입함.",
            "박지희_일기.txt": "박지희의 일기: '이진호가 식사를 거의 하지 않는 것이 이상하다. 그리고 항상 같은 옷만 입는다. 개인 위생에 문제가 있는 건지...'"
        },
        "cafeteria": {
            "식단표.txt": "식단표: 주간 메뉴 목록. 김르탄이 특별 식단을 요청했었음.",
            "재고_목록.txt": "재고 목록: 식품 보급 상태. 일부 식재료가 정기적으로 사라지는 현상 발생.",
            "CCTV.txt": "CCTV: 02:15에 김르탄이 커피를 마시는 모습. 신종우가 그에게 다가가 대화하는 장면.",
            "청소_일지.txt": "청소 일지: 03-14 저녁 식사 후 이진호가 음식을 거의 먹지 않고 버림. 오성택은 항상 다른 사람들보다 두 배 많은 양을 먹음."
        },
        "comms": {
            "통신_기록.txt": "통신 기록: 최근 송수신 내역",
            "장비_상태.txt": "장비 상태: 모든 시스템 정상 작동 중",
            "통신_매뉴얼.txt": "통신 매뉴얼: 표준 프로토콜 설명서",
            "주파수_로그.txt": "주파수 로그: 심야에 미확인 주파수 사용 기록"
        },
        "security": {
            "보안_로그.txt": "보안 로그: 02:30에 실험실 구역 카메라 일시적 정전. 김혜성의 보안 코드로 시스템 접근 기록.",
            "카메라_제어.txt": "카메라 제어 장치: 수동 전원 차단 기능이 있음. 최근 허원영이 이 시스템을 검사함.",
            "출입_기록.txt": "출입 기록: 여러 선원들의 야간 이동 경로. 02:25-02:35 사이 실험실 주변 기록 삭제됨.",
            "열감지_스캔.txt": "열감지 스캔 결과: 선원들의 체온 데이터. 이진호의 체온이 비정상적으로 낮다."
        },
        "maintenance": {
            "수리_도구.txt": "수리 도구: 끈 모양의 케이블 타이 한 묶음이 없어짐",
            "환기구_지도.txt": "환기구 지도: 모든 구역을 연결하는 환기 시스템",
            "작업_지시서.txt": "작업 지시서: 03-15 02:30 - 오성택이 정비실 근무 예정",
            "이상_물질.txt": "환기구 필터에서 발견된 녹색 점액 물질 - 정체 불명"
        }
    }

    # 각 장소에 물건/증거 파일 생성
    for location, items in location_items.items():
        for item_name, content in items.items():
            with open(f"{LOCATIONS_DIR}/{location}/{item_name}", "w") as f:
                f.write(content)

    # 실험실에 숨겨진 증거 추가
    with open(f"{LOCATIONS_DIR}/lab/.숨겨진_메모.txt", "w") as f:
        f.write("노트가 지워져서 앞쪽은 읽을 수 없다.\n")
        f.write("....의 혈액 샘플을 채취해 분석했는데, 결과가 충격적이다.\n")
        f.write("인간의 DNA가 아니다. 더 조사가 필요하다.\n")
        f.write("- 김르탄")

    # 실험실에 엘리스인 분석 파일 추가
    with open(f"{LOCATIONS_DIR}/lab/엘리스인_분석.txt", "w") as f:
        f.write("엘리스인 생물학적 특성 분석 보고서:\n\n")
        f.write("1. 체온: 지구인보다 약 2-3도 낮은 체온을 유지함. 열감지 스캐너로 식별 가능.\n\n")
        f.write("2. 생리학적 특징: 산소 소비량이 적고, 질소 기반 호흡 가능. 식사량이 지구인의 1/3 수준.\n\n")
        f.write("3. 신체적 특징: 눈의 망막이 특수 세포로 구성되어 있어 스트레스 상황에서 녹색으로 빛남.\n\n")
        f.write("4. DNA 구조: 삼중 나선 구조로, 지구 생명체의 이중 나선과 완전히 다름. 특수 단백질 분석 필요.\n\n")
        f.write("5. 행동 패턴: 수면이 거의 필요 없으며, 감정 표현이 제한적. 사회적 상호작용 시 패턴화된 행동 보임.\n\n")
        f.write("6. 특수 능력: 제한적 형태 변형 가능. 인간 외형 모방 시 일부 특징(체온, 눈 색상)은 완벽히 숨기지 못함.\n\n")
        f.write("7. 약점: 고농도 산소 환경에 취약함. 특정 주파수의 소리(18-20kHz)에 심각한 고통을 느낌.\n\n")
        f.write("8. 분비물: 스트레스 상황에서 특수 녹색 점액 분비. 이 물질은 지구상 어떤 원소와도 일치하지 않음.\n\n")
        f.write("9. 통신 방식: 양자 얽힘 기술을 이용한 즉각적 장거리 통신 가능. 일반 통신 장비로는 감지 불가능.\n\n")
        f.write("10. 수명: 지구인의 약 3배. 노화 징후가 거의 나타나지 않아 외형적 나이 판단이 어려움.\n\n")
        f.write("경고: 이 정보는 최고 기밀. 엘리스인은 고도로 지능적이며 위험한 종족으로, 우주 식민지 확장을 위해 침략적 성향을 보임.")

    # 통신실에 숨겨진 증거 추가
    os.mkdir(f"{LOCATIONS_DIR}/comms/.비밀")
    with open(f"{LOCATIONS_DIR}/comms/.비밀/외계_통신.txt", "w") as f:
        f.write("엘리스 함대 사령부에 보내는 보고서:\n")
        f.write("침투 성공. 인간 '이진호'로 위장 중.\n")
        f.write("우주선 좌표 및 방어 시스템 정보 전송 완료.\n")
        f.write("침략 준비 완료 시 신호 전송 예정.\n")
        f.write("과학책임자가 의심하기 시작함. 제거 필요.\n")

    # 선원 숙소 B구역에 숨겨진 증거 추가
    with open(f"{LOCATIONS_DIR}/quarters2/.비밀_장치.txt", "w") as f:
        f.write("이진호의 침대 밑에서 발견한 이상한 장치.\n")
        f.write("지구의 기술이 아닌 것으로 보임.\n")
        f.write("엘리스 문자로 추정되는 기호가 새겨져 있음.\n")

    # 선원 숙소 A구역에 추가 파일
    with open(f"{LOCATIONS_DIR}/quarters1/이강욱_캐비닛.txt", "w") as f:
        f.write("선장의 개인 캐비닛에는 우주선 비상 프로토콜 매뉴얼과 함께\n")
        f.write("가족 사진이 보관되어 있다. 사진 뒷면에는 '항상 너희를 생각하며'\n")
        f.write("라는 메시지가 적혀있다. 또한 특별한 열쇠가 보관되어 있는데,\n")
        f.write("이것은 선장만이 접근할 수 있는 비상 시스템을 위한 것으로 보인다.\n")
        f.write("캐비닛 깊숙한 곳에는 '엘리스 성운 탐사 계획안'이라는 제목의 문서가 숨겨져 있다.\n")

    with open(f"{LOCATIONS_DIR}/quarters1/조재휘_작업대.txt", "w") as f:
        f.write("엔지니어의 작업대에는 다양한 엔진 부품 모형과 설계도가 있다.\n")
        f.write("특히 눈에 띄는 것은 우주선 엔진의 축소 모형으로, 정교하게 제작되었다.\n")
        f.write("작업대 서랍에는 개인 일지가 있는데, 최근 엔진 이상에 대한 걱정이 기록되어 있다.\n")
        f.write("또한 가족에게 보내려던 미완성 편지도 발견된다.\n")
        f.write("작업대 아래 숨겨진 공간에는 김르탄의 연구 자료 사본이 보관되어 있다.\n")
        f.write("'그가 무엇을 발견했는지 알아내야 한다'라는 메모가 붙어있다.\n")

    with open(f"{LOCATIONS_DIR}/quarters1/신종우_의료가방.txt", "w") as f:
        f.write("의사의 개인 의료 가방에는 기본적인 응급 처치 도구와 함께\n")
        f.write("몇 가지 특수 약품이 들어있다. 특히 강력한 진정제와 수면제가 보인다.\n")
        f.write("의료 기록 패드에는 각 선원들의 건강 상태가 기록되어 있으며,\n")
        f.write("특이하게도 이진호의 기록에는 '비정상적 생체 지표' 메모가 있다.\n")
        f.write("가방 바닥에는 '김르탄 제거 계획'이라는 제목의 메모가 숨겨져 있다.\n")
        f.write("내용은 암호화되어 있어 읽을 수 없다.\n")

    # 선원 숙소 B구역에 추가 파일
    with open(f"{LOCATIONS_DIR}/quarters2/김르탄_연구자료.txt", "w") as f:
        f.write("김르탄의 개인 연구 자료에는 다양한 생물학적 분석 결과가 있다.\n")
        f.write("특히 눈에 띄는 것은 '미확인 DNA 구조 분석'이라는 제목의 파일이다.\n")
        f.write("파일 내용은 암호화되어 있어 읽을 수 없지만, 메모에는\n")
        f.write("'이것은 인간의 DNA가 아니다. 더 조사 필요' 라고 적혀있다.\n")

    with open(f"{LOCATIONS_DIR}/quarters2/오성택_공구함.txt", "w") as f:
        f.write("정비사의 공구함에는 다양한 맞춤형 도구들이 정리되어 있다.\n")
        f.write("특이한 점은 몇몇 도구가 최근에 사용된 흔적이 있으며,\n")
        f.write("특히 절단기와 용접 도구에 녹색 물질이 묻어있다.\n")
        f.write("공구함 바닥에는 '환기구 수리 완료 - 03-14' 메모가 있다.\n")
        f.write("공구함 뒤쪽에 숨겨진 공간에는 실험실 접근 코드와 함께\n")
        f.write("김르탄의 연구실 도면이 보관되어 있다. 특정 지점이 표시되어 있다.\n")

    with open(f"{LOCATIONS_DIR}/quarters2/허원영_컴퓨터.txt", "w") as f:
        f.write("AI 전문가의 개인 컴퓨터는 고급 암호화로 보호되어 있다.\n")
        f.write("화면 보호기에는 복잡한 알고리즘 다이어그램이 표시되어 있다.\n")
        f.write("컴퓨터 옆에는 '이상 행동 패턴 감지 프로그램' 설계 노트가 있으며,\n")
        f.write("메모에는 '선원 중 한 명의 행동이 AI 예측 모델과 일치하지 않음' 이라고 적혀있다.\n")
        f.write("컴퓨터 하단에 숨겨진 드라이브에는 '선원 행동 조작 프로토콜'이라는 파일이 있다.\n")
        f.write("파일에는 인간 행동을 모방하는 AI 알고리즘에 대한 내용이 담겨있다.\n")

    # 의무실에 추가 파일 생성
    with open(f"{LOCATIONS_DIR}/medbay/엘리스인_의학_보고서.txt", "w") as f:
        f.write("기밀 의학 보고서 - 엘리스인 생체 특성\n\n")
        f.write("1. 혈액 분석: 엘리스인의 혈액은 구리 기반으로, 산소와 결합 시 녹색을 띰. 인간의 철 기반 혈액과 완전히 다름.\n\n")
        f.write("2. 면역 체계: 지구 병원체에 완전 면역. 그러나 특정 지구 항생제에 심각한 알레르기 반응 보임.\n\n")
        f.write("3. 재생 능력: 경미한 상처는 수 시간 내 자가 치유. 절단된 사지도 수주 내 재생 가능.\n\n")
        f.write("4. 심장 구조: 3개의 심장 챔버를 가짐. 하나가 손상되어도 생존 가능.\n\n")
        f.write("5. 호흡 체계: 산소와 질소 모두 처리 가능한 이중 호흡기 시스템. 진공 상태에서도 짧은 시간 생존 가능.\n\n")
        f.write("6. 신경계: 인간보다 2배 빠른 신경 반응 속도. 통증 인지 능력 조절 가능.\n\n")
        f.write("7. 감각 기관: 자외선과 적외선 영역까지 볼 수 있는 확장된 시각 범위. 초음파 감지 능력 보유.\n\n")
        f.write("8. 소화 시스템: 거의 모든 유기물 소화 가능. 식사 빈도가 적으며, 에너지 효율이 매우 높음.\n\n")
        f.write("9. 생식: 무성 생식과 유성 생식 모두 가능. 성체가 되기까지 지구 시간으로 약 50년 소요.\n\n")
        f.write("10. 식별 방법: 표준 의료 스캔에서 비정상적 장기 배열 감지됨. DNA 검사 시 즉시 비인간으로 판별 가능.\n\n")
        f.write("주의사항: 엘리스인은 인간 DNA를 흡수하여 외형을 모방할 수 있음. 정기적인 DNA 스캔으로만 확실히 식별 가능.")

    # 함교에 추가 파일 생성
    with open(f"{LOCATIONS_DIR}/bridge/엘리스_성운_보고서.txt", "w") as f:
        f.write("엘리스 성운 탐사 보고서 - 기밀 등급 알파\n\n")
        f.write("위치: 오리온 팔 외곽, 지구로부터 약 1,200광년 거리\n\n")
        f.write("탐사 역사: 최초 발견(2156년), 첫 유인 탐사(2170년), 첫 접촉 사건(2172년)\n\n")
        f.write("행성계: 7개의 주요 행성, 그 중 3개가 엘리스인 거주지로 확인됨\n\n")
        f.write("문명 수준: 지구보다 약 500년 앞선 기술 수준. 항성간 여행, 양자 통신, 생체 공학 분야 특히 발달.\n\n")
        f.write("사회 구조: 계급제 사회. 과학자 계층이 지배층을 형성. 군사적으로 매우 발달되어 있음.\n\n")
        f.write("외교 관계: 공식적으로는 지구와 평화 협정 체결(2175년). 그러나 비공식 정보에 따르면 침략 계획 의심됨.\n\n")
        f.write("위험 평가: 매우 높음. 엘리스인들은 자원 부족으로 새로운 거주 행성을 찾고 있으며, 지구가 주요 목표로 추정됨.\n\n")
        f.write("침투 사례: 지난 5년간 인간 우주선과 식민지에 대한 20건 이상의 침투 시도 확인. 대부분 엘리스인 스파이가 인간으로 위장.\n\n")
        f.write("방어 프로토콜: 모든 우주선과 기지에 DNA 스캐너와 체온 감지기 설치 권고. 엘리스인 생체 신호 데이터베이스 구축 중.\n\n")
        f.write("경고: 이 정보는 최고 기밀. 엘리스인의 침략 계획이 확인될 경우, 즉시 지구 방위군에 통보할 것.")

@app.command()
def start():
    """
    우주선 살인 사건 미스터리 게임을 시작합니다.
    """
    if os.path.exists(GAME_DIR):
        shutil.rmtree(GAME_DIR)
    
    create_game_files()
    
    console.print("[bold green]우주선 살인 사건 미스터리에 오신 것을 환영합니다![/bold green]")
    console.print("\n2184년 3월 15일, 우주선 '스파르타호'에서 과학책임자 김르탄이 살해당한 채 발견되었습니다.")
    console.print("당신은 이 사건을 조사하는 수사관입니다.")
    console.print("\n[bold yellow]조사를 위해 다음 Unix 명령어들을 사용하세요:[/bold yellow]")
    console.print("- ls: 파일 목록 확인")
    console.print("- ls -la: 숨겨진 파일을 포함한 모든 파일 확인")
    console.print("- cat: 파일 내용 읽기")
    console.print("- cd: 디렉토리 이동")
    console.print("- stat: 파일의 상세 정보 확인")
    console.print("- find: 파일 찾기")
    console.print("\n[bold cyan]장소 설명:[/bold cyan]")
    for loc_key, loc_name in LOCATIONS.items():
        console.print(f"- {loc_key}: {loc_name}")
    
    console.print("\n증거를 모두 수집한 후, 범인을 지목하려면:")
    console.print("python main.py solve [범인_이름]")
    console.print("\n[bold red]게임 시작![/bold red]")

@app.command()
def solve(suspect: str):
    """
    범인을 지목합니다.
    """
    if suspect.lower() == "이진호" or suspect.lower() == "통신담당_이진호":
        console.print("[bold green]축하합니다! 범인을 찾았습니다![/bold green]")
        console.print("\n[bold yellow]사건 요약:[/bold yellow]")
        console.print("이진호는 사실 인간의 모습으로 위장한 엘리스 종족의 외계인이었습니다!")
        console.print("그는 엘리스 성운에서 온 침략자로, 지구 방어 시스템의 약점을 찾기 위해")
        console.print("우주선에 침투하여 정보를 수집하고 있었습니다.")
        console.print("김르탄(과학책임자)이 이진호의 정체를 발견하고 증거를 수집하여")
        console.print("선장에게 보고하려 하자, 이진호는 자신의 정체가 탄로나는 것을 막기 위해")
        console.print("김르탄을 살해했습니다.")
        console.print("\n증거들:")
        console.print("1. 빨간색 섬유 (통신 담당자 유니폼 색상)")
        console.print("2. 실험실에서 발견된 김르탄의 숨겨진 메모")
        console.print("3. 보안 카메라에 찍힌 이진호의 행적")
        console.print("4. 통신실의 비밀 통신 기록")
        console.print("5. 선원 숙소에서 발견된 이상한 장치")
        console.print("6. 의무실의 비정상적인 건강검진 기록")
        console.print("7. 환기구에서 발견된 녹색 점액")
        console.print("8. DNA 분석 결과 - 인간과 다른 구조")
        console.print("\n[bold red]경고: 엘리스 종족의 침략자가 아직 더 있을 수 있습니다! 우주선의 보안을 강화하세요![/bold red]")
    else:
        console.print("[bold red]틀렸습니다! 다시 증거를 검토해보세요.[/bold red]")

if __name__ == "__main__":
    app()