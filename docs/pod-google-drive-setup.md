# Pod에서 구글 드라이브 연결하기 (운영 절차서)

작성: 2026-09-18

상태: `절차 — 아직 실제 계정으로 실행 안 함`

> 이 문서는 사용자가 직접 실행하는 절차서라 한국어로 작성한다. 에이전트가 읽는 설계 문서
> (`pc-less-cloud-studio-plan.md` 등)는 기존대로 영어를 유지한다.

클라우드 세션에서 드라이브는 durable 저장소다. 가중치와 캐릭터 입력이 내려오고, 세션 산출물이
올라간다. 설계 배경은 [PC 없는 클라우드 스튜디오 계획](pc-less-cloud-studio-plan.md) 참고.

## 핵심 제약

pod에는 브라우저도, 콘솔 앞에 앉은 사람도 없다. 그래서 대화형 OAuth를 끝낼 수 없다.
모든 해법은 결국 같은 모양이다 — **브라우저가 있는 곳에서 딱 한 번 인증하고, 그 결과를
이후 모든 pod에 시크릿으로 주입한다.** 이미지에 굽지 말 것, 커밋하지 말 것.

## 데스크톱 드라이브 앱과는 무관하다

PC에 구글 드라이브 데스크톱 앱이 깔려 동기화가 돌고 있어도 이 절차는 그대로 필요하다.
둘은 서로 아무 관계가 없다.

- **데스크톱 앱**은 그 PC의 폴더를 동기화하는 윈도우 프로그램이다. 자기 인증을 앱 내부에
  가지고 있고, 그것을 꺼내 다른 기기에서 쓸 수 없다.
- **pod에 필요한 것**은 드라이브 API를 HTTPS로 호출할 refresh token 문자열 하나다. OAuth를
  한 번 밟아야만 생긴다.

### PC에서 인증하는 이유는 하나뿐이다

rclone은 승인 결과를 `127.0.0.1:53682` 로 되돌려받는다. 그래서 **브라우저와 rclone이 같은
기기에** 있어야 한다. 폰 브라우저로 하면 폰의 루프백을 찾아가 실패한다. PC는 단지 "브라우저와
rclone이 둘 다 있는 기기"일 뿐이고, 맥이든 다른 PC든 무방하다.

```text
어느 기기에서든 한 번:  rclone config -> 브라우저 승인 -> token 생성
                                                    |
                                       이 텍스트만 pod으로 이동
                                                    |
        이후 모든 pod:  그 token으로 드라이브 접근. 그 기기는 더 이상 관여하지 않는다
```

3분이고 평생 한 번이다. 그 PC가 중계하거나 켜져 있어야 하는 구조가 아니다.

### 동기화 폴더 제외를 권함

PC에서 드라이브 동기화가 켜져 있으면, 나중에 PC를 켰을 때 pod이 생성한 출력물이 전부
내려받아질 수 있다. 영상이면 수십 GB가 된다. pod 출력 경로(`xai/outputs` 등)는 데스크톱 앱의
선택적 동기화에서 **제외**해 두는 편이 좋다.

---

## 0단계 — 본인 구글 OAuth client ID 먼저 발급

다른 거 하기 전에 이것부터. rclone에 기본 내장된 공용 client ID는 구글이 강하게 속도 제한을
걸어둔다. "드라이브가 느리네"라는 결론이 사실은 그 제한을 측정한 것인 경우가 흔하다.

> **주의: 드라이브의 "프로젝트"가 아니다.**
> 구글 드라이브 화면에 보이는 `프로젝트`는 Gemini가 파일을 검색하게 하는 별개 기능이다.
> 여기서 필요한 것은 **Google Cloud Console**(`console.cloud.google.com`)의 클라우드
> 프로젝트다. 서로 아무 관계가 없다.

`https://console.cloud.google.com` 에 같은 계정으로 접속한 뒤:

1. **프로젝트 생성** — 상단 프로젝트 선택기 → `새 프로젝트` → 이름 입력 → 만들기
2. **Drive API 사용 설정** — `https://console.cloud.google.com/apis/library/drive.googleapis.com`
   에서 `사용 설정`. (메뉴 경로는 `API 및 서비스` → `라이브러리` → "Google Drive API")
3. **OAuth 동의 화면** — `API 및 서비스` → `OAuth 동의 화면`. 최근 콘솔에서는
   **`Google Auth Platform`** 아래로 이동했을 수 있다. `외부` 선택, 앱 이름과 지원 이메일 입력,
   **테스트 사용자에 본인 계정 추가**.
4. **클라이언트 ID 발급** — `사용자 인증 정보` → `사용자 인증 정보 만들기` →
   `OAuth 클라이언트 ID` → 애플리케이션 유형 **데스크톱 앱** → 만들기.
   client ID와 client secret 보관.
5. **앱 게시** — 동의 화면에서 `앱 게시`(프로덕션으로 푸시)를 누른다.

### 다운로드되는 JSON 파일에 대해

4단계에서 구글이 JSON 파일 하나를 내려준다. 정상이다. 안에 `installed.client_id` 와
`installed.client_secret` 이 들어 있고, **필요한 것은 그 두 값뿐**이다.

혼동하기 쉬운 점:

- 이것은 **서비스 계정 키가 아니다** (그건 경로 C 전용이고 개인 계정에는 쓰지 않는다);
- 이것은 **아직 토큰이 아니다.** 1단계 인증을 거쳐야 refresh token이 생긴다.

JSON 파일과 이후 생성되는 `rclone.conf` 는 둘 다 자격증명이다. Git에 넣지 않는다.

### 현재 상태 (2026-09-18)

동의 화면은 **`테스트` 상태이고, 계정 하나를 테스트 사용자로 등록**해 진행했다. 게시는 아직
하지 않았다. 측정과 수동 작업에는 지장이 없다.

**따라서 refresh token은 발급 후 약 7일에 만료된다.** 일주일쯤 지나 pod의 드라이브 접근이
갑자기 실패하면 원인은 자격증명 만료이지 네트워크나 rclone 설정이 아니다. 다른 곳을 뒤지지 말 것.

무인 운용을 시작하기 전에 **앱 게시 → 인증 1회 재실행**으로 만료되지 않는 토큰을 받는다.
게시 자체는 기존 client ID를 무효화하지 않으므로 client ID를 다시 만들 필요는 없지만, 이미
발급된 토큰의 만료 시점은 발급 시 정해지므로 재인증은 필요하다.

또 하나 흔한 오해: 테스트 사용자로 등록되지 않은 계정으로 로그인하면 `403 access_denied`
("개발자가 승인한 테스터만 액세스할 수 있습니다")로 막히는데, 이 화면에는 `고급` 링크가 없다.
`고급`이 나오는 "확인되지 않은 앱" 경고는 그 관문을 통과한 **다음** 단계다.

### 5번을 빠뜨리면 매주 끊긴다

동의 화면이 **"테스트" 상태로 남아 있으면 외부 앱의 refresh token이 7일 후 만료된다.** 그러면
pod의 드라이브 연결이 일주일마다 실패하고, 무인 운용이 불가능해진다. 본인만 쓰는 앱이라
게시할 때 "확인되지 않은 앱" 경고가 뜨지만 그대로 진행하면 되고, 게시 후에는 그 7일 규칙이
적용되지 않는다.

속도 측정을 하려면 이 단계가 반드시 먼저다. 공용 ID로 재면 드라이브가 아니라 rclone의 제한을
재게 된다.

---

## 1단계 — 딱 한 번 인증

상황에 맞는 경로 하나만 고르면 된다.

### 경로 A — 브라우저 있는 PC를 쓸 수 있을 때 (제일 간단)

rclone은 **단일 실행파일**이다. 설치 프로그램도 의존성도 없으니 시스템에 무언가를 얹는 부담을
가질 필요가 없다. 윈도우 PowerShell 기준:

```powershell
cd ~\Downloads
Invoke-WebRequest https://downloads.rclone.org/rclone-current-windows-amd64.zip -OutFile rclone.zip
Expand-Archive rclone.zip -DestinationPath .
cd rclone-*-windows-amd64
.\rclone.exe config
```

`winget install Rclone.Rclone` 도 동일하게 동작한다. 작업이 끝나면 받은 폴더는 지워도 되고,
생성된 설정은 `C:\Users\<사용자>\AppData\Roaming\rclone\rclone.conf` 에 따로 남는다.

대화형 프롬프트에는 이렇게 답한다:

```bash
rclone config
# n) New remote      name> gdrive      Storage> drive
# client_id / client_secret> 0단계에서 만든 값
# scope> 1 (full access)
# service_account_file> (비워둠)
# Edit advanced config? n
# Use web browser to automatically authenticate? y
```

```
# Storage> 는 "drive" 입력하면 찾아준다
# scope> 1 (full access)
# service_account_file> 엔터로 비워둠
# Configure this as a Shared Drive? n
```

브라우저에서 승인한 뒤 확인한다:

```bash
rclone about gdrive:        # 용량이 보이면 성공
rclone config show gdrive   # client_id / client_secret / token 세 줄이 최종 산출물
```

`token = {...}` 한 줄이 refresh token을 담은 실제 결과물이다. 2단계로.

### 경로 B — 폰만 있을 때

첫 pod을 띄우고 테일넷에 넣은 뒤, pod에서 위와 같은 `rclone config`를 실행하고 자동 브라우저
옵션을 고른다. rclone은 콜백을 `127.0.0.1:53682`에서 받으므로, 인증하는 동안만 테일넷으로 열어준다:

```bash
socat TCP-LISTEN:53682,fork,reuseaddr TCP:127.0.0.1:53682 &
```

폰에서 `http://<pod의 테일넷 IP>:53682/auth` 를 열어 승인하고, 끝나면 위 프로세스를 종료한다.
pod은 테일넷 안에서만 닿으므로 외부에 노출되는 것은 없다.

### 경로 C — Google Workspace + 공유 드라이브가 있을 때

**서비스 계정**을 쓴다. Cloud Console에서 만들고 JSON 키를 받은 뒤, 그 서비스 계정 주소를
공유 드라이브 멤버로 추가한다. 토큰 갱신도 대화형 절차도 영영 필요 없다.

개인 Gmail 계정의 내 드라이브에는 서비스 계정을 쓰지 말 것. 서비스 계정은 자체 저장 용량이
없어서, 거기에 파일을 만들려 하면 실패한다. 파일 소유권이 공유 드라이브에 있을 때만 동작한다.

---

## 2단계 — 인증 결과를 pod 시크릿으로 바꾸기

rclone은 `RCLONE_CONFIG_<리모트>_<옵션>` 환경변수만으로 리모트 전체를 읽는다. 설정 파일을
이미지에 넣을 필요가 없다.

```text
RCLONE_CONFIG_GDRIVE_TYPE=drive
RCLONE_CONFIG_GDRIVE_CLIENT_ID=<0단계 값>
RCLONE_CONFIG_GDRIVE_CLIENT_SECRET=<0단계 값>
RCLONE_CONFIG_GDRIVE_TOKEN=<rclone.conf 의 token JSON 그대로>
RCLONE_CONFIG_GDRIVE_ROOT_FOLDER_ID=<선택: 폴더 하나로 범위 제한>
```

`token`은 생성된 `~/.config/rclone/rclone.conf`에서 **그대로 복사**한다. refresh token이 들어
있어서 이후 추가 인증 없이 계속 동작한다. 런처가 시크릿을 두는 곳에 넣고 pod에 환경변수로
전달한다. **자격증명이다 — Git에도, 이미지에도, 실행 기록에도 넣지 않는다.**

`ROOT_FOLDER_ID`는 설정해 두는 편이 낫다. pod이 계정 전체가 아니라 폴더 하나만 보게 된다.

---

## 3단계 — mount 말고 copy/sync

```bash
# 입력 (부팅 시)
rclone copy gdrive:xai/inputs /workspace/inputs \
  --transfers 8 --checkers 16 --fast-list

# 가중치 (이번 세션에 필요한 프로필만)
rclone copy gdrive:xai/models/<프로필> /workspace/models \
  --transfers 8 --drive-chunk-size 256M

# 출력 (세션 내내 계속)
rclone copy /workspace/outputs gdrive:xai/outputs/<세션ID> \
  --transfers 8 --drive-chunk-size 256M --update
```

`rclone mount`보다 `copy`/`sync`를 쓴다. mount는 편하지만 큰 순차 쓰기와 쓰기 중인 SQLite에
취약하고, 멈추면 전송 재시도가 아니라 생성 실패가 된다.

출력 복사는 종료 직전이 아니라 **세션 내내 짧은 주기로** 돌린다. 연속 동기화가 있어야 짧은
유휴 타임아웃을 안심하고 걸 수 있다.

### 튜닝

- `--drive-chunk-size` 가 큰 파일 처리량을 좌우한다. 256M에서 시작. 전송 하나당 RAM을 쓴다.
- `--fast-list` 는 파일 많은 디렉터리에서 API 호출을 줄인다.
- 드라이브는 업로드 하루 750GB 상한이 있다. 같은 큰 파일을 하루에 여러 번 받으면 파일별
  다운로드 쿼터에 걸릴 수 있다.

---

## 4단계 — 믿기 전에 검증

```bash
rclone about gdrive:                       # 자격증명 동작, 용량 확인
rclone lsd gdrive:xai                      # 폴더 구조 확인
rclone check /workspace/outputs gdrive:xai/outputs/<세션ID>
```

`rclone check`는 양쪽 해시를 비교한다. **종료는 copy 명령의 종료 코드가 아니라 check 통과를
조건으로 해야 한다.** 이 프로젝트의 "검증된 내보내기 후에만 파괴" 규칙이 여기에도 적용된다.

---

## 5단계 — 속도 측정 (아키텍처 생존 조건)

드라이브가 느리면 단순히 느려지는 게 아니라 **설계가 성립하지 않는다.** 연속 출력 동기화가
생성 속도를 못 따라가면 짧은 유휴 타임아웃이 위험해지고, 종료 전 최종 내보내기가 GPU 과금 중에
돌아간다. 그래서 **워커 이미지를 만들기 전에** 측정한다.

임계 경로는 다운로드가 아니라 **업로드**다. 산출물이 pod을 떠나야 하고 종료가 거기 걸려 있다.
드라이브는 보통 업로드가 다운로드보다 느리다.

그리고 진짜 위험한 건 **작은 파일이 많은 경우**다. 파일마다 API 호출이 붙어서 PNG 200장이
5GB 영상 하나보다 훨씬 느릴 수 있다. 여기 산출물은 주로 이미지 배치다. 네 가지를 다 잰다:

```bash
# 업로드 — 큰 파일 하나 (영상 세션 종료 시간)
time rclone copy /workspace/big.mp4 gdrive:xai/bench/ --drive-chunk-size 256M

# 업로드 — 작은 파일 다발  ← 가장 위험한 케이스
time rclone copy /workspace/batch-200-png gdrive:xai/bench/batch --transfers 16 --checkers 32

# 다운로드 — 큰 파일 하나 (가중치 수급)
time rclone copy gdrive:xai/bench/big.mp4 /tmp/ --transfers 8 --drive-chunk-size 256M

# 다운로드 — 작은 파일 다발 (캐릭터 시트, 레퍼런스)
time rclone copy gdrive:xai/bench/batch /tmp/batch --transfers 16 --fast-list

# 공개 가중치는 허브와 비교
HF_HUB_ENABLE_HF_TRANSFER=1 time hf download <repo> <비슷한크기파일> --local-dir /tmp/
```

전부 0단계의 본인 client ID로. **GPU는 필요 없다** — 기존 네트워크 볼륨을 점검하고 삭제하는
그 저렴한 CPU pod에서 같이 하면 된다.

### 드라이브가 너무 느리면

설계는 살아남고, 전송 수단만 바뀐다.

1. **작은 파일은 묶어서 올린다.** 배치마다 tar 하나면 파일별 API 오버헤드가 사라진다. 갤러리는
   어차피 pod 로컬 디스크를 읽으므로 드라이브에는 묶음만 있으면 된다. 이것만으로 최악의 경우가
   해결될 가능성이 높다.
2. **세션 중 주고받기는 S3 호환 오브젝트 스토리지로.** Cloudflare R2는 egress 요금이 없고
   100GB에 월 $1.5 수준이다. `docs/render-broker.md`가 이미 *"one provider-neutral
   S3-compatible interface"* 를 예정해 뒀으므로 새 의존성이 아니라 예약된 경로다.
3. **역할 분리**: 오브젝트 스토리지는 세션 중 전송, 드라이브는 장기 보관.

측정된 MB/s는 클라우드 계획 문서의 미측정 항목 절에 기록한다. 이 숫자가 워커 이미지를 무엇과
통신하도록 만들지를 결정한다.
