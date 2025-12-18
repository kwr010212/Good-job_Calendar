"""
담당: 곽건우
역할: 일정 데이터 저장 / 불러오기

설명:
- 일정 데이터를 JSON 파일로 저장
- 프로그램 실행 시 파일에서 일정 로드
- 메모리 ↔ 파일 간 데이터 동기화 담당
"""

import json
import os
from typing import List, Dict, Any

# JSON 데이터 파일 경로 (현재 파일과 같은 디렉토리에 저장)
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

# 메모리에 일정 데이터를 저장하는 딕셔너리
# key: 일정 id, value: 일정 정보(dict)
_store: Dict[int, Dict[str, Any]] = {}

# 다음 일정 id 값 (파일 로드 시 기존 데이터 기준으로 갱신)
_next_id = 1


def _load_file():
    """
    JSON 파일에서 일정 데이터를 불러와 메모리에 저장한다.
    - 파일이 없거나 손상된 경우 빈 데이터로 초기화
    - 불러온 데이터의 최대 id를 기준으로 다음 id 값 설정
    """
    global _store, _next_id

    if not os.path.exists(DATA_FILE):
        _store = {}
        _next_id = 1
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = []

    # 리스트 데이터를 id 기준 딕셔너리로 변환
    _store = {int(item["id"]): item for item in data if "id" in item}

    # 최대 id를 기준으로 다음 id 설정
    _next_id = max(_store.keys()) + 1 if _store else 1


def _save_file():
    """
    메모리에 저장된 데이터를 JSON 파일로 기록한다.
    - 디렉토리가 없으면 자동 생성
    - UTF-8로 저장, 들여쓰기 적용
    """
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(list(_store.values()), f, ensure_ascii=False, indent=2)


def load_all() -> List[Dict[str, Any]]:
    """
    모든 일정 데이터를 리스트로 반환한다.
    - 외부 모듈은 이 함수만 사용 (내부 구현 직접 접근 제한)
    """
    _load_file()
    return list(_store.values())