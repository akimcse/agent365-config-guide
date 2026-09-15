# -*- coding: utf-8 -*-
import json, os, html, re

BASE = r"C:\Users\hyunakim\OneDrive - Microsoft\문서\Microsoft Scout\01_guide\agent365-webguide"
deck = json.load(open(os.path.join(BASE, "deck.json"), encoding="utf-8"))

def table_of(slide_no):
    for sh in deck[slide_no-1]["shapes"]:
        if sh["kind"] == "table":
            return sh["table"]
    return None

CH = [
 dict(id="ch0", num="0", name="에이전트 생성", intro=3, range=(4,17),
      lead="Copilot Studio(New experience)에서 실습용 에이전트를 만들고, 지침·지식·도구를 구성한 뒤 Teams / Microsoft 365 Copilot 채널로 게시하고 관리자 승인까지 제출하는 단계입니다. 이후 1~7장의 모든 관리·보안 시나리오는 여기서 만든 에이전트를 대상으로 진행합니다."),
 dict(id="ch1", num="1", name="에이전트 승인 및 전사 배포", intro=18, range=(19,25),
      lead="제작자가 제출한 에이전트를 AI 관리자가 검토·승인하고, 조직 카탈로그(Microsoft Store)에 게시해 전사에 배포하는 단계입니다. 승인 심사에서는 제작자·업무 목적·지식·도구·요청 권한을 함께 확인합니다."),
 dict(id="ch2", num="2", name="에이전트 인벤토리 확인", intro=26, range=(27,30),
      lead="테넌트에 존재하는 에이전트를 레지스트리에서 조회하고, 각 에이전트의 소유자·지식·도구·권한·채널 구성과 실제 사용량을 확인하는 단계입니다. 등록되어 있다는 것과 실제로 쓰이고 있다는 것은 다르므로 두 가지를 분리해서 봅니다."),
 dict(id="ch3", num="3", name="에이전트 차단", intro=31, range=(32,37),
      lead="문제가 있는 에이전트를 즉시 사용 불가 상태로 만들고, 사용자 화면에서 실제로 차단됐는지 확인한 뒤 복구하는 단계입니다. 차단은 삭제나 Agent ID 인증 중지와는 구분되는 조치입니다."),
 dict(id="ch4", num="4", name="에이전트에 대한 조건부 접근제어", intro=38, range=(39,47),
      lead="Entra 조건부 액세스 정책을 에이전트(Agent ID)와 에이전트가 사용하는 리소스에 적용하고, 로그인 로그로 정책 평가 결과를 검증하는 단계입니다."),
 dict(id="ch5", num="5", name="에이전트 리스크 탐지", intro=48, range=(49,64),
      lead="Purview 내부 위험 관리(IRM)에서 에이전트 정책을 만들어 위험 신호를 수집하고, 에이전트 경고를 확인하는 단계입니다. 감사 로그 수집이 켜져 있어야 지표·경고가 생성됩니다."),
 dict(id="ch6", num="6", name="에이전트 런타임 보호", intro=65, range=(66,80),
      lead="Defender AI 보안과 Power Platform 위협 탐지를 연결해, Copilot Studio 에이전트의 도구 호출·프롬프트를 실시간으로 검사하고 차단하는 단계입니다. 커넥터 설정 → 인증용 앱 생성 → 환경 연결 → 보호 정책 순으로 진행합니다."),
 dict(id="ch7", num="7", name="에이전트 트래픽 모니터링", intro=81, range=(82,86),
      lead="Global Secure Access for Agents(preview)를 환경 단위로 켜고, Entra의 Gen AI 인사이트 로그에서 에이전트가 주고받은 실제 트래픽(요청·응답)을 조회하는 단계입니다."),
]

DESC = {
 4:"New Copilot Studio 우측 상단의 환경 선택기에서 실습에 사용할 Power Platform 환경을 먼저 고정합니다. 여기서 선택한 환경이 6장(런타임 보호)·7장(트래픽 모니터링)의 <b>환경 단위 설정 대상</b>과 동일해야 하므로, 처음부터 실습 환경을 정해두는 것이 중요합니다. 해당 환경에 대한 제작자(Maker) 이상의 역할이 필요합니다.",
 5:"Agents 화면에서 <b>New agent</b>를 선택해 템플릿이 아닌 빈 에이전트로 시작합니다. 빈 에이전트로 시작해야 지침·지식·도구를 하나씩 통제하면서 붙일 수 있고, 이후 승인 심사에서 무엇이 왜 붙었는지 설명하기 쉽습니다. 이 가이드에서는 <code>Agent365-Guide-Demo</code>라는 이름을 사용합니다.",
 6:"① 에이전트 이름, ② 지침(Instructions), ③ 모델·행동 설정 순으로 입력합니다. New experience에서는 모델과 오케스트레이션 설정 위치가 기존 UI와 달라 <code>Settings &gt; AI &amp; behavior</code>에서 확인해야 하며, 기존의 '생성형 AI' 토글과는 구분됩니다. 지침은 1장의 관리자 승인 심사에서 <b>업무 목적을 판단하는 근거</b>가 되므로 구체적으로 작성합니다.",
 7:"<code>Build &gt; Add knowledge</code>에서 SharePoint·OneDrive·Dataverse 등 지식 원본을 연결합니다. 여기서 붙인 지식은 1장의 관리자 승인 화면과 2장의 인벤토리 <b>데이터 &amp; 도구</b> 탭에 그대로 노출되므로, 민감한 사이트를 연결할 때는 사전 검토가 필요합니다.",
 8:"<code>Build &gt; Add tool &gt; Model Context Protocol (MCP)</code> 카탈로그에서 필요한 도구를 연결합니다. MCP 도구는 런타임에 실제로 호출되는 지점이므로, 5장(리스크 탐지)·6장(런타임 보호)·7장(트래픽 모니터링)에서 <b>탐지·보호·로깅의 실제 대상</b>이 됩니다.",
 9:"Preview(테스트) 패널에서 한국어 프롬프트로 실행해 지식 인용과 도구 호출이 정상인지 확인합니다. 단, 테스트 패널에서 발생한 활동은 2장에서 보는 <b>활성 사용자·세션 통계에는 집계되지 않습니다</b>. 실제 사용량 확인은 게시된 채널에서 실행한 결과로 판단해야 합니다.",
 10:"구성이 끝나면 게시 다이얼로그에서 채널 추가를 시작합니다. 게시는 '에이전트를 저장하는 것'이 아니라 <b>사용자에게 노출될 경로를 여는 것</b>이라는 점을 구분합니다.",
 11:"채널 선택기에서 <b>Teams 및 Microsoft 365 Copilot</b>을 선택합니다. 이 채널이 연결되어 있어야 이후 1장의 조직 카탈로그 배포, 3장의 차단 결과를 사용자 화면에서 확인할 수 있습니다.",
 12:"① 사용할 채널을 확인하고 ② 표시(가용성) 범위를 선택합니다. 이 단계에서 선택한 범위가 관리자 승인 요청 여부를 결정합니다.",
 13:"Teams + Microsoft 365 채널 게시가 완료된 상태입니다. <b>게시 완료가 곧 조직 카탈로그 승인·전사 배포 완료를 뜻하지는 않습니다</b>. 조직 전체 노출은 다음 단계의 관리자 승인을 거쳐야 합니다.",
 14:"① 채널의 가용성 옵션을 열고 ② <b>내 조직의 모든 사람에게 표시</b>를 선택합니다. 이 선택이 AI 관리자에게 전달되는 승인 요청을 생성합니다.",
 15:"제출 전 검토 화면에서 제작자, 설명, 연결된 지식·도구, 요청 권한 요약을 확인합니다. 여기 표시되는 내용이 관리자 검토 화면에 그대로 전달되므로, 설명이 비어 있으면 승인이 지연될 수 있습니다.",
 16:"조직 공개 여부를 묻는 확인 대화상자에서 <b>예</b>를 선택하면 승인 요청이 제출됩니다.",
 17:"제출 후에는 <b>승인 대기</b> 상태로 표시됩니다. 새로 고침으로 요청 상태를 확인하며, 이 시점부터는 제작자가 아니라 AI 관리자의 작업(1장)으로 넘어갑니다.",

 19:"AI 관리자 계정으로 <code>Microsoft 365 관리 센터 &gt; 에이전트 &gt; 모든 에이전트 &gt; 요청</code>으로 이동해 ① 요청 목록에서 ② 대상 요청을 엽니다. 이 메뉴가 보이지 않으면 Entra에서 <b>AI 관리자</b> 역할이 할당되었는지 먼저 확인합니다.",
 20:"요청 상세에서 ① <b>Microsoft Store에 게시</b> 버튼을 선택해 게시 마법사를 시작합니다. 이 화면에서 제작자·업무 목적·지식·도구·요청 권한을 검토하고, 부적절하면 제출을 거부할 수 있습니다.",
 21:"① 설치 가능 대상과 ② 사전 설치 대상을 지정한 뒤 ③ 다음으로 진행합니다. <b>설치 가능</b>은 사용자가 원할 때 직접 추가하는 방식이고, <b>사전 설치</b>는 대상 사용자에게 자동으로 배포되는 방식이므로 영향 범위가 다릅니다.",
 22:"배포 시 적용될 앱 정책 템플릿을 확인합니다. 조직에 이미 적용 중인 앱 설정 정책이 있는 경우 여기서 함께 확인됩니다.",
 23:"권한 검토 화면입니다. 이 사례에서는 <b>필요한 권한 없음</b>으로 표시됐지만, 이는 에이전트의 모든 MCP 도구가 무권한으로 실행된다는 뜻이 <b>아닙니다</b>. 도구별 인증·동의는 별도로 적용되며, 실제 데이터 접근은 도구 수준에서 다시 통제됩니다.",
 24:"최종 검토 화면에서 대상·권한·정책을 한 번 더 확인한 뒤 게시합니다.",
 25:"관리자 처리가 완료된 상태입니다. 배포 직후에는 Teams / Microsoft 365 Copilot 사용자 화면에 반영되기까지 시간이 걸릴 수 있으므로, 사용자 실행 확인은 잠시 후 다시 시도합니다.",

 27:"① <code>에이전트 &gt; 모든 에이전트 &gt; 레지스트리</code>로 이동해 ② <b>Platform = Copilot Studio</b>로 필터링합니다. 레지스트리는 테넌트에 등록된 에이전트의 단일 목록이며, <b>등록되어 있다는 사실이 실제로 사용 중이라는 뜻은 아닙니다</b>.",
 28:"에이전트 상세의 <b>세부 정보</b>에서 소유자, 게시 채널, 상태, 그리고 해당 에이전트의 <b>Entra Agent ID</b>를 확인합니다. 이 Agent ID는 4장에서 조건부 액세스 대상으로 지정하고 로그인 로그와 대조할 때 사용하는 핵심 식별자입니다. 지식·도구(Data &amp; tools) 구성은 여기서 조회만 하고, 변경은 Copilot Studio에서 수행합니다.",
 29:"① 조회 기간을 지정하고 ② 활성 사용자·세션 지표를 확인합니다. 관리 센터의 활성 지표는 <b>게시된 채널에서 발생한 실사용</b>을 기준으로 집계됩니다.",
 30:"Copilot Studio의 <b>모니터</b>에서 세션·사용자 추이를 확인합니다. ① 조회 기간, ② 활성 사용자 보기를 확인하되 <b>기본 시간대가 UTC</b>인 점과 <b>테스트 패널 활동이 제외</b>되는 점을 감안해 해석합니다.",

 32:"차단 전 에이전트 상세 화면입니다. 차단 이전 상태(채널, 설치 대상, 상태 값)를 먼저 기록해 두면 이후 복구가 정상적으로 됐는지 비교할 수 있습니다.",
 33:"① <b>에이전트 차단</b>을 선택하고 ② 저장합니다. 차단은 에이전트를 삭제하거나 Agent ID의 인증 자체를 중지하는 것과는 다른 조치로, 구성은 유지한 채 <b>사용만 즉시 막는</b> 방식입니다.",
 34:"저장 후 관리 센터에서 상태가 차단으로 바뀐 것을 확인합니다.",
 35:"관리자 화면뿐 아니라 <b>일반 사용자 화면(Teams / Microsoft 365 Copilot)</b>에서 실제로 실행이 막히는지 확인합니다. 기존 진입점, 신규 설치, 새 대화 각각에 대해 확인하고 채널별 결과를 기록해 두는 것이 좋습니다.",
 36:"복구를 위해 다시 에이전트 상세로 이동합니다.",
 37:"① <b>에이전트 차단 해제</b>를 선택하고 ② 저장합니다. 해제 후에는 설치·가용성 범위가 차단 전과 동일한지, 사용자 실행이 정상으로 돌아왔는지 함께 재확인합니다.",

 39:"<code>Entra 관리 센터 &gt; 보호 &gt; 조건부 액세스 &gt; 정책</code>에서 ① 새 정책을 만들고 ② 이름을 지정합니다. 이 작업에는 <b>조건부 액세스 관리자</b> 역할이 필요합니다.",
 40:"할당 단계에서 정책 적용 대상을 지정합니다(①~④). 에이전트는 사람 사용자와 달리 <b>Agent ID</b>로 지정하며, 사용자 대상 정책과 섞이지 않도록 대상 범위를 명확히 분리합니다.",
 41:"① 대상 리소스에서 ② 에이전트가 실제로 호출하는 커넥터·리소스를 지정합니다. 에이전트만 지정하고 실제 접근 리소스를 빠뜨리면 <b>커넥터 호출이 정책 평가에서 누락</b>될 수 있습니다.",
 42:"조건(네트워크·디바이스·위치 등)을 구성합니다(①~⑤). 에이전트는 사용자 디바이스가 없는 워크로드 형태로 동작하므로, 디바이스 기반 조건을 그대로 적용하면 의도치 않은 차단이 발생할 수 있습니다.",
 43:"액세스 제어에서 허용/차단과 요구 제어를 지정합니다(①~③).",
 44:"① 정책 사용 상태를 지정하고 ② 생성합니다. 운영 적용 전에는 <b>보고서 전용(Report-only)</b>으로 먼저 영향도를 확인하는 것을 권장하며, 보고서 전용은 <b>실제로 차단하지 않습니다</b>.",
 45:"정책 평가를 검증하기 위해 ① 대상 에이전트를 확인하고 ② Teams에서 에이전트와 커넥터를 실제로 실행해 트래픽을 발생시킵니다.",
 46:"<code>Entra &gt; 모니터링 및 상태 &gt; 로그인 로그</code>에서 ①~③ 순으로 조회합니다. 사용자 로그인이 아닌 <b>서비스 주체 / 에이전트 로그인</b> 영역을 확인해야 에이전트 트래픽이 보입니다.",
 47:"로그인 상세에서 ① Agent ID·리소스·시각과 ② 조건부 액세스 평가 결과를 대조합니다. 정책이 실제로 적용됐는지는 이 <b>조건부 액세스 탭의 결과 값</b>으로 판단합니다.",

 49:"<code>Purview &gt; 감사 &gt; 감사 수집 상태</code>에서 감사 로그 수집이 켜져 있는지 먼저 확인합니다. <b>감사 로그가 꺼져 있으면 IRM 정책을 만들어도 분석할 활동 이벤트 자체가 없어 지표·경고가 생성되지 않습니다.</b>",
 50:"<code>내부 위험 관리 &gt; 정책</code>에서 ①~④ 순으로 에이전트 정책 생성을 시작합니다. 이 작업에는 <b>내부자 위험 관리 분석가</b> 또는 <b>조사자</b> 역할이 필요합니다.",
 51:"정책 템플릿을 선택합니다. 에이전트 전용 템플릿을 선택하면 에이전트 활동 지표가 기본 세트로 구성됩니다.",
 52:"① 정책 이름, ② 설명, ③ 다음 순으로 입력합니다. 이름에 적용 범위를 드러내면 이후 경고 분류에 도움이 됩니다.",
 53:"정책을 적용할 에이전트 범위를 지정합니다. 현재 UI에서는 ① <b>모든 에이전트</b>가 선택되어 있고 ② 특정 에이전트 선택은 비활성화되어 있습니다. 따라서 정책 이름에 Demo가 들어 있어도 <b>단일 에이전트 범위가 아니라 테넌트 전체 범위</b>로 적용된다는 점에 유의합니다.",
 54:"우선순위로 다룰 콘텐츠(민감도 레이블·사이트·파일 유형 등)를 선택합니다(①②).",
 55:"앞서 선택한 콘텐츠 각각에 대해 세부 항목을 추가로 지정합니다(①~④). 우선순위 콘텐츠는 위험 점수 가중치에 직접 영향을 줍니다.",
 56:"알림(경고)을 생성할 범위를 지정합니다(①②).",
 57:"경고를 유발할 이벤트 트리거를 선택합니다(①②). 에이전트의 어떤 행위를 위험 신호의 시작점으로 볼 것인지 정하는 단계입니다.",
 58:"트리거 임계값을 지정합니다(①~③). <b>초기에는 경고가 실제로 생성되는지 확인하기 위해 임계값을 최대한 낮게 잡고</b>, 오탐 추이를 보면서 사내 환경에 맞게 점차 올리는 방식을 권장합니다.",
 59:"표시기(Indicator) 단계에서 선택한 총 표시기 수(4/4)와 에이전트 지표 분류를 확인합니다. 화면에 선택되어 있다고 해서 <b>해당 이벤트가 실제로 수집·탐지되고 있다는 보장은 아니며</b>, 실제 동작 여부는 경고와 활동 증거로 별도 확인해야 합니다.",
 60:"탐지 옵션의 <b>위험 점수 부스터</b>에는 에이전트 활동이 그날 평균 활동을 상회하는 경우 등의 조건이 표시됩니다. 앞서 설정한 <b>트리거 임계값·지표 임계값과는 별개</b>이므로 구분해서 검토합니다.",
 61:"최종 검토 후 정책을 생성합니다.",
 62:"정책 생성이 완료된 상태입니다. <b>정책 생성 후 실제 경고가 표시되기까지 최대 24시간이 걸릴 수 있습니다.</b>",
 63:"<code>내부 위험 관리 &gt; 에이전트 &gt; 경고</code>에서 ① 시간·상태·심각도 필터, ② 항목 수, ③ 결과를 확인합니다. 이 실습 시점에서는 <b>사용 가능한 경고가 0건</b>이었고 경보 상세·활동 탐색기·증거는 열 수 없었습니다. 이 경우 임계값과 감사 수집 상태, 에이전트 실사용량을 먼저 점검하는 것이 순서입니다.",
 64:"경고가 생성된 경우의 확인 경로입니다(①~③). 대상 에이전트, 심각도, 활동 순서를 함께 확인해 어떤 도구 호출이 위험 신호로 잡혔는지 추적합니다.",

 66:"<code>Defender &gt; 설정 &gt; AI 보안 &gt; 시작</code>에서 ①~③ 순으로 이동한 뒤 <b>Microsoft 365 커넥터</b>를 구성합니다. 이 커넥터가 Agent 365·Microsoft 365 활동과 Entra 관리 이벤트를 수집하는 입구 역할을 합니다. <b>애플리케이션 관리자 / 보안 관리자</b> 역할이 필요합니다.",
 67:"수집할 구성 요소를 선택합니다(①②). Agent 365와 Microsoft 365가 모두 연결 대상인지 확인합니다.",
 68:"커넥터 연결이 완료된 상태입니다.",
 69:"<b>Copilot Studio 실시간 보호</b> 항목으로 이동해 ①② 순으로 통합을 엽니다. 이 화면에 표시되는 <b>Power Platform 통합용 엔드포인트 URL은 반드시 복사해 둡니다</b>. <a class=\"xref\" data-target=\"s72\">4단계(PowerPlatform 보안 설정)</a>에서 그대로 입력해야 합니다.",
 70:"관리자 권한으로 Windows PowerShell을 열고, 스크립트가 있는 디렉터리에서 <code>Create-CopilotWebhookApp.ps1</code>을 실행합니다. ① <b>TenantId</b>는 Entra 개요의 테넌트 ID, ② <b>Endpoint</b>는 <a class=\"xref\" data-target=\"s69\">2단계(Copilot Studio 연결)</a>에서 복사한 URL을 넣고, <code>DisplayName</code>과 <code>FICName</code>은 조직 고유 값으로 지정합니다. 이 스크립트는 Defender가 Power Platform을 호출할 때 사용할 앱 등록과 <b>페더레이션 자격 증명(FIC)</b>을 함께 만듭니다.",
 71:"스크립트 실행 결과로 생성된 앱 등록을 Entra에서 확인합니다(①~③). 여기 표시된 <b>앱(클라이언트) ID도 복사해 둡니다</b> — <a class=\"xref\" data-target=\"s72\">4단계(PowerPlatform 보안 설정)</a>의 연결 설정에 입력합니다.",
 72:"<code>Power Platform 관리 센터 &gt; 보안 &gt; 위협 탐지 &gt; 추가 위협 탐지</code>로 이동합니다(①~③). <b>Power Platform 관리자</b> 역할이 필요합니다.",
 73:"① 실습 환경(Agent-Demo)을 선택하고 ② 설정을 엽니다. <b>보호 연결은 환경 단위</b>이므로 다른 환경이나 기본 환경을 선택하지 않도록 주의합니다.",
 74:"연결 설정에서 ①~⑤ 순으로 값을 입력합니다. <b>앱 ID는 <a class=\"xref\" data-target=\"s70\">3단계(인증용 앱 구성)</a>에서 생성한 값</b>, <b>엔드포인트는 <a class=\"xref\" data-target=\"s69\">2단계(Copilot Studio 연결)</a>에서 복사한 URL</b>을 사용합니다. 검사 실패(오류) 시 동작을 <b>Allow</b>로 둘지 <b>Block</b>으로 둘지 선택한 뒤 저장합니다. Block은 보호 수준이 높지만 탐지 서비스 장애 시 에이전트 실행이 함께 막힐 수 있습니다.",
 75:"6-1 ~ 6-4 설정이 모두 연결된 상태입니다. 여기까지가 <b>탐지 파이프라인 구성</b>이고, 실제 차단 동작은 다음 단계의 보호 정책에서 결정됩니다.",
 76:"<code>Defender &gt; 설정 &gt; AI 보안 &gt; 정책 및 규칙</code>에서 ①② 순으로 커스텀 실시간 보호 정책을 만듭니다. <b>기본(Default) 정책은 Audit</b>이므로 차단이 필요하면 별도 커스텀 정책을 만들어야 합니다.",
 77:"정책 이름과 적용 범위를 지정합니다(①②).",
 78:"탐지 대상과 조치(Block/Audit)를 지정합니다(①~③).",
 79:"정책 검토 후 생성합니다. <b>현재 Copilot Studio 에이전트에 대해서는 차단(Block) 규칙을 생성·적용하더라도 그 차단 동작이 로그로 기록되지 않습니다</b>. 이는 공식 문서에 명시된 알려진 제한 사항으로, 정책 생성 여부와 무관하게 Copilot Studio 대상 차단 이벤트는 현재 로그·헌팅에서 조회되지 않습니다.",
 80:"<b>프롬프트 증거 수집</b> 설정입니다. 켜면 경고 조사 시 실제 프롬프트 내용을 근거로 볼 수 있지만, 프롬프트 본문이 저장되므로 민감정보 취급 정책과 함께 검토해야 합니다.",

 82:"<code>Power Platform 관리 센터 &gt; 보안 &gt; ID 및 액세스 &gt; 에이전트에 대한 전역 보안 액세스</code>로 이동합니다(①~③). <b>전역 보안 액세스 관리자</b> 역할이 필요합니다.",
 83:"① 실습 환경을 선택하고 ② 설정을 엽니다. GSA 적용도 <b>환경 단위</b>이므로 같은 환경의 다른 에이전트에도 함께 영향이 갑니다.",
 84:"① <b>Enable</b>을 On으로 바꾸고 ② 저장합니다. 이 시점부터 해당 환경 에이전트의 아웃바운드 트래픽이 Global Secure Access를 경유합니다.",
 85:"<code>Entra &gt; 전역 보안 액세스 &gt; 모니터링</code>에서 활성화 상태를 확인합니다(①②).",
 86:"<b>Gen AI 인사이트 로그</b>에서 에이전트가 실제로 주고받은 트래픽을 조회합니다(①②). <b>Event ID·Transaction ID로 상관 분석</b>하면 하나의 실행에 대한 요청·응답을 이어서 볼 수 있으며, MCP <code>tools/call</code>의 요청 본문과 응답까지 확인할 수 있습니다. 로그 반영에는 지연이 있을 수 있습니다.",
}

# Real, copyable code blocks that replace a code screenshot on a slide.
CODE = {
 70: ('PowerShell',
r'''.\Create-CopilotWebhookApp.ps1 `
  -TenantId "11111111-2222-3333-4444-555555555555" `
  -Endpoint "https://provider.example.com/threat_detection/copilot" `
  -DisplayName "Copilot Security Integration - Production" `
  -FICName "ProductionFIC"'''),
}

def title_of(n):
    for sh in deck[n-1]["shapes"]:
        if sh["kind"] == "text" and sh["name"] in ("제목 1",) or (sh["kind"]=="text" and "title" in sh["name"].lower()):
            return sh["text"].replace("\n", " ").strip()
    return f"슬라이드 {n}"

def esc(s): return html.escape(s)

parts = []
nav = []
SKIP = {63}  # slides excluded from the guide
for c in CH:
    nav.append(f'<a href="#{c["id"]}" data-sec="{c["id"]}"><span class="n">{c["num"]}</span><span>{esc(c["name"])}</span></a>')

def anchor_for(c, firstcol):
    fc = firstcol.strip()
    if not fc.isdigit():
        return None
    for n in range(c["range"][0], c["range"][1]+1):
        if n in SKIP:
            continue
        t = title_of(n)
        if t.startswith(f"{c['num']}-{fc}.") or t.startswith(f"{c['num']}-{fc} "):
            return n
    return None

for c in CH:
    tbl = [list(r) for r in table_of(c["intro"])]
    if tbl and not tbl[0][-1].strip():
        for r in tbl:
            tail = r.pop().strip()
            if tail:
                r[-1] = (r[-1].rstrip() + "\n" + tail) if r[-1].strip() else tail
    hdr = tbl[0]
    ncol = len(hdr)
    ths = "".join(f"<th>{esc(x.replace(chr(10),' '))}</th>" for x in hdr)
    trs = []
    for r in tbl[1:]:
        anc = anchor_for(c, r[0])
        tds = "".join("<td>" + esc(x).replace("\n", "<br>") + "</td>" for x in r)
        if anc:
            trs.append(f'<tr class="jump" data-target="s{anc}" tabindex="0">{tds}</tr>')
        else:
            trs.append(f"<tr>{tds}</tr>")
    steps = []
    substep = {}
    valid_steps = {int(r[0]) for r in tbl[1:] if r[0].strip().isdigit() and int(r[0]) > 0}
    last_valid = None
    for k, n in enumerate(range(c["range"][0], c["range"][1]+1), 1):
        if n in SKIP:
            continue
        t = title_of(n)
        ct = re.sub(r'^\s*\d+\s*-\s*\d+(\s*[~∼]\s*\d+\s*-\s*\d+)?\.?\s*', '', t).strip().rstrip('|').strip()
        m = re.match(r'^\s*((?:\d+\s*-\s*\d+\s*[~∼]?\s*)+)', t)
        if m:
            pairs = re.findall(r'\d+\s*-\s*(\d+)', m.group(1))
            step = int(pairs[-1]) if pairs else k
        else:
            step = k
        if valid_steps and step not in valid_steps:
            step = last_valid if last_valid is not None else min(valid_steps)
        last_valid = step
        substep[step] = substep.get(step, 0) + 1
        label = f"{step}-{substep[step]}"
        d = DESC.get(n, "")
        code_html = ""
        if n in CODE:
            lang, src = CODE[n]
            code_html = (f'<div class="code"><div class="code-head"><span>{esc(lang)}</span>'
                         f'<button class="copy-btn" type="button">복사</button></div>'
                         f'<pre><code>{esc(src)}</code></pre></div>')
        if os.path.exists(os.path.join(BASE, "img", f"slide-{n:02d}a.png")):
            imgs = "".join(
                f'<a href="img/slide-{n:02d}{p}.png" target="_blank" rel="noopener"><img loading="lazy" src="img/slide-{n:02d}{p}.png" alt="{esc(ct)}"></a>'
                for p in ("a", "b"))
        else:
            imgs = f'<a href="img/slide-{n:02d}.png" target="_blank" rel="noopener"><img loading="lazy" src="img/slide-{n:02d}.png" alt="{esc(ct)}"></a>'
        steps.append(f"""
      <figure class="fig" id="s{n}">
        <div class="fig-title"><span class="fig-num">{label}</span>{esc(ct)}</div>
        {code_html}
        {imgs}
      </figure>
      <div class="note">{d}</div>""")
    parts.append(f"""
  <section id="{c['id']}" class="page">
    <div class="hero">
      <span class="tag">Chapter {c['num']} · Microsoft Agent 365</span>
      <h1>{c['num']}. {esc(c['name'])}</h1>
      <p>{esc(c['lead'])}</p>
    </div>
    <h2 class="ov-h">전체 순서 한눈에 보기</h2>
    <div class="tw"><table><thead><tr>{ths}</tr></thead><tbody>{''.join(trs)}</tbody></table></div>
    <h2 class="ov-h">단계별 상세</h2>
    {''.join(steps)}
    <div class="pagenav">__PN{c['num']}__</div>
  </section>""")

# pager links
for i, c in enumerate(CH):
    prev_html = ""
    nxt_html = ""
    if i > 0:
        p = CH[i-1]
        prev_html = f'<a class="prv" href="#{p["id"]}" data-go="{p["id"]}"><span class="lbl">← 이전</span><br>{p["num"]}. {esc(p["name"])}</a>'
    else:
        prev_html = '<span class="pn-empty"></span>'
    if i < len(CH)-1:
        nx = CH[i+1]
        nxt_html = f'<a class="nxt" href="#{nx["id"]}" data-go="{nx["id"]}"><span class="lbl">다음 →</span><br>{nx["num"]}. {esc(nx["name"])}</a>'
    else:
        nxt_html = '<span class="pn-empty"></span>'
    parts[i] = parts[i].replace(f"__PN{c['num']}__", prev_html + nxt_html)

CSS = """
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");
:root{--bg:#f6f8fb;--surface:#fff;--surface-2:#eef1f4;--border:#e2e6ec;--text:#1f2328;--text-soft:#57606a;--accent:#0f6cbd;--accent-2:#8a5cf6;--accent-pink:#d63aa0;--code-bg:#1e2430;--code-text:#e6edf3;--crit:#b3261e;--low:#3a7d34;--shadow:0 1px 3px rgba(20,30,50,.06),0 8px 24px rgba(20,30,50,.06);--radius:14px;}
html[data-theme="dark"]{--bg:#0f141b;--surface:#171d26;--surface-2:#212a35;--border:#2b3542;--text:#e6edf3;--text-soft:#9aa7b4;--accent:#58a6ff;--accent-2:#b18cff;--accent-pink:#ff6bbd;--code-bg:#0b0e13;--code-text:#e6edf3;--crit:#f0655d;--low:#6bbf5f;--shadow:0 1px 3px rgba(0,0,0,.5),0 8px 24px rgba(0,0,0,.4);}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{margin:0;font-family:Pretendard,-apple-system,BlinkMacSystemFont,"Segoe UI","Malgun Gothic",sans-serif;background:var(--bg);color:var(--text);line-height:1.7;font-size:16px;}
a{color:var(--accent);text-decoration:none;}
a:hover{text-decoration:underline;}
code{background:var(--surface-2);padding:2px 6px;border-radius:5px;font-family:"Cascadia Code",Consolas,monospace;font-size:13.5px;color:#b0387c;}
html[data-theme="dark"] code{color:#ff9dd4;}
.layout{display:flex;min-height:100vh;}
.sidebar{width:290px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);padding:26px 18px;position:sticky;top:0;height:100vh;overflow-y:auto;display:flex;flex-direction:column;}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:14px;margin-bottom:8px;letter-spacing:-.3px;line-height:1.3;}
.brand .dot{width:24px;height:24px;border-radius:8px;background:linear-gradient(135deg,var(--accent) 0%,var(--accent-2) 55%,var(--accent-pink) 100%);flex-shrink:0;}
.brand-sub{font-size:12px;color:var(--text-soft);margin:0 0 22px 34px;}
.nav-group{margin-bottom:18px;}
.nav-group h4{font-size:11px;text-transform:uppercase;letter-spacing:.8px;color:var(--accent);margin:0 0 8px 8px;font-weight:700;}
.nav-group a{display:flex;gap:10px;align-items:center;padding:8px 10px;border-radius:8px;color:var(--text);font-size:14px;margin-bottom:2px;}
.nav-group a:hover{background:var(--surface-2);text-decoration:none;}
.nav-group a.active{background:linear-gradient(135deg,rgba(15,108,189,.12),rgba(138,92,246,.12));color:var(--accent);font-weight:600;}
.nav-group a .n{flex:0 0 22px;height:22px;display:grid;place-items:center;border-radius:6px;background:var(--surface-2);border:1px solid var(--border);font-size:12px;font-weight:700;}
.nav-group a.active .n{background:linear-gradient(135deg,var(--accent),var(--accent-2));color:#fff;border-color:transparent;}
.nav-parent{font-weight:600;}
.nav-children{margin:2px 0 2px 10px;padding-left:12px;border-left:1.5px solid var(--border);}
.nav-sub .n{flex:0 0 20px;height:20px;font-size:11px;}
.nav-sub{font-size:13.5px;padding:7px 10px;}
.theme-toggle{display:inline-flex;align-items:center;gap:6px;margin:auto 8px 2px;align-self:flex-start;padding:8px 15px;background:var(--surface-2);border:1px solid var(--border);border-radius:999px;color:var(--text);font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;}
.theme-toggle:hover{border-color:var(--accent);background:var(--surface);}
.main{flex:1;min-width:0;}
.content{max-width:940px;margin:0 auto;padding:46px 40px 90px;}
.page{display:none;}
.page.active{display:block;animation:fade .18s ease;}
@keyframes fade{from{opacity:0;transform:translateY(4px);}to{opacity:1;transform:none;}}
.hero{background:linear-gradient(135deg,#0f6cbd 0%,#6a4bd8 55%,#c0389a 100%);color:#fff;border-radius:var(--radius);padding:36px 34px;margin-bottom:30px;box-shadow:var(--shadow);}
.hero .tag{display:inline-block;background:rgba(255,255,255,.18);backdrop-filter:blur(4px);padding:4px 12px;border-radius:999px;font-size:12px;font-weight:600;margin-bottom:14px;}
.hero h1{margin:0 0 12px;font-size:29px;line-height:1.25;letter-spacing:-.5px;}
.hero p{margin:0;font-size:15.5px;opacity:.95;}
h2.ov-h{font-size:20px;letter-spacing:-.3px;margin:38px 0 14px;padding:4px 0 10px 14px;position:relative;border-bottom:1px solid var(--border);}
h2.ov-h::before{content:"";position:absolute;left:0;top:2px;bottom:10px;width:5px;border-radius:5px;background:linear-gradient(180deg,var(--accent),var(--accent-2) 55%,var(--accent-pink));}
.ov-sub{color:var(--text-soft);font-size:14px;margin:0 0 12px;}
.page-lead{color:var(--text-soft);font-size:15.5px;margin:0 0 8px;}
.pname{font-weight:700;white-space:nowrap;}
.portal-link{font-family:"Cascadia Code",Consolas,monospace;font-size:12.5px;white-space:nowrap;}
.scope-box{background:var(--surface);border:1px solid var(--border);border-left:4px solid var(--accent-2);border-radius:10px;padding:16px 18px;box-shadow:var(--shadow);margin:6px 0 8px;}
.scope-box p{margin:0 0 10px;font-size:14.5px;}
.cta-link{display:inline-block;margin-top:4px;padding:9px 16px;border-radius:8px;font-weight:600;font-size:14px;color:#fff;background:linear-gradient(135deg,var(--accent),var(--accent-2));text-decoration:none;}
.cta-link:hover{text-decoration:none;opacity:.92;}
.download-btn{display:inline-flex;align-items:center;gap:8px;margin:2px 0 14px;padding:9px 15px;border-radius:8px;font-weight:600;font-size:13.5px;color:var(--accent);background:var(--surface);border:1px solid var(--border);text-decoration:none;}
.download-btn:hover{text-decoration:none;border-color:var(--accent);background:var(--surface-2);}
.method{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px 18px;box-shadow:var(--shadow);margin:0 0 12px;}
.method-head{display:flex;align-items:center;gap:10px;font-weight:700;font-size:15px;margin-bottom:6px;}
.method-no{flex:0 0 24px;height:24px;display:inline-flex;align-items:center;justify-content:center;border-radius:7px;background:linear-gradient(135deg,var(--accent),var(--accent-2));color:#fff;font-size:13px;}
.method p{margin:6px 0;font-size:14px;}
.method-cond{color:var(--text-soft);font-size:13px;}
.rec{font-size:11px;font-weight:700;color:#fff;background:var(--low,#3a7d34);border-radius:999px;padding:2px 9px;margin-left:2px;}
table{width:100%;border-collapse:collapse;margin:6px 0 8px;font-size:14px;background:var(--surface);border-radius:10px;overflow:hidden;box-shadow:var(--shadow);}
.tw{overflow-x:auto;}
th,td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--border);vertical-align:top;}
th{background:var(--surface-2);font-weight:600;font-size:13px;white-space:nowrap;}
td:first-child,th:first-child{text-align:center;font-weight:700;width:42px;color:var(--accent);}
tr:last-child td{border-bottom:none;}
tr.jump{cursor:pointer;transition:background .12s;}
tr.jump td:last-child::after{content:"→ 이동";color:var(--accent);font-weight:700;float:right;opacity:0;transition:opacity .12s;padding-left:8px;font-size:12px;}
tr.jump:hover td,tr.jump:focus td{background:linear-gradient(135deg,rgba(15,108,189,.08),rgba(138,92,246,.08));}
tr.jump:hover td:last-child::after,tr.jump:focus td:last-child::after{opacity:1;}
tr.jump:focus{outline:none;}
@keyframes flash{0%{box-shadow:0 0 0 3px var(--accent) inset;}100%{box-shadow:0 0 0 0 transparent inset;}}
figure.fig.flash img{animation:flash 1.2s ease-out;}
figure.fig{margin:24px 0 6px;}
figure.fig img{display:block;width:100%;height:auto;border:1px solid var(--border);border-radius:10px;box-shadow:var(--shadow);background:var(--surface);}
figure.fig a + a img{margin-top:14px;}
.fig-title{display:flex;align-items:center;gap:10px;font-size:15.5px;font-weight:600;margin:0 0 10px;letter-spacing:-.2px;color:var(--text);}
.fig-num{flex:0 0 auto;min-width:34px;height:26px;padding:0 9px;display:inline-flex;align-items:center;justify-content:center;border-radius:8px;background:linear-gradient(135deg,var(--accent),var(--accent-2));color:#fff;font-size:13px;font-weight:700;letter-spacing:.2px;}
.code{margin:14px 0 4px;border:1px solid var(--border);border-radius:10px;overflow:hidden;box-shadow:var(--shadow);}
.code-head{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;background:var(--surface-2);border-bottom:1px solid var(--border);font-size:12.5px;font-weight:700;color:var(--text-soft);}
.copy-btn{font:inherit;font-size:12px;font-weight:600;padding:4px 12px;border-radius:7px;border:1px solid var(--border);background:var(--surface);color:var(--text);cursor:pointer;}
.copy-btn:hover{border-color:var(--accent);color:var(--accent);}
.copy-btn.done{border-color:var(--success);color:var(--success);}
.code pre{margin:0;background:var(--code-bg);color:var(--code-text);padding:14px 16px;overflow-x:auto;font-family:"Cascadia Code",Consolas,monospace;font-size:13px;line-height:1.6;}
.code pre code{background:none;padding:0;color:inherit;font-size:inherit;white-space:pre;}
.note{background:#eef4fb;border-left:4px solid var(--accent);border-radius:10px;padding:13px 16px;margin:8px 0 26px;font-size:14.5px;color:var(--text);}
html[data-theme="dark"] .note{background:#13243a;}
.note b{color:var(--text);}
.xref{color:var(--accent);font-weight:600;text-decoration:none;border-bottom:1px dashed var(--accent);cursor:pointer;}
.xref:hover{text-decoration:none;background:var(--accent-soft,rgba(15,108,189,.1));border-radius:4px;}
html[data-theme="dark"] .xref{color:var(--accent);}
.pagenav{display:flex;justify-content:space-between;gap:14px;margin-top:44px;}
.pagenav a{flex:1;background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px 18px;box-shadow:var(--shadow);color:var(--text);}
.pagenav a:hover{text-decoration:none;border-color:var(--accent);}
.pagenav a.nxt{text-align:right;}
.pagenav .lbl{font-size:12px;color:var(--text-soft);}
.pn-empty{flex:1;}
.footer{margin-top:50px;padding-top:18px;border-top:1px solid var(--border);color:var(--text-soft);font-size:13px;}
@media(max-width:860px){.layout{flex-direction:column;}.sidebar{width:100%;height:auto;position:static;border-right:none;border-bottom:1px solid var(--border);}.content{padding:30px 20px 60px;}}
"""

HTML = """<!DOCTYPE html>
<html lang="ko" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agent 365 초기 설정 및 구성 가이드</title>
<script>
(()=>{const p=new URLSearchParams(location.search).get("scoutTheme");const s=localStorage&&localStorage.getItem?localStorage.getItem("a365theme"):null;const t=p||s||(window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light");document.documentElement.setAttribute("data-theme",t);})();
</script>
<style>__CSS__</style>
</head>
<body>
<div class="layout">
<aside class="sidebar">
  <div class="brand"><span class="dot"></span><span>Agent 365 초기 설정 및 구성 가이드</span></div>
  <div class="brand-sub">Copilot Studio · 관리 · 보안 실습 (0–7)</div>
  <nav class="nav-group">
    <h4>가이드</h4>
    <a href="#overview" data-sec="overview" class="nav-parent"><span class="n">◆</span><span>Copilot Studio 에이전트</span></a>
    <div class="nav-children">
    __NAV__
    </div>
  </nav>
  <button class="theme-toggle" id="tt">🌓 테마 전환</button>
</aside>
<main class="main"><div class="content">
  __SECTIONS__
  <div class="footer">Microsoft Agent 365 초기 설정 및 구성 가이드 · 스크린샷은 Copilot Studio(New experience) 실습 기준 · 각 장 상단 표가 전체 순서입니다.</div>
</div></main>
</div>
<script>
const links=Array.from(document.querySelectorAll('.nav-group a'));
const ids=links.map(a=>a.dataset.sec);
function show(id,push){if(!ids.includes(id))id=ids[0];
 document.querySelectorAll('.page').forEach(s=>s.classList.toggle('active',s.id===id));
 links.forEach(a=>a.classList.toggle('active',a.dataset.sec===id));
 if(push)history.replaceState(null,'','#'+id);
 window.scrollTo({top:0,behavior:'smooth'});}
links.forEach(a=>a.addEventListener('click',e=>{e.preventDefault();show(a.dataset.sec,true);}));
document.querySelectorAll('[data-go]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();show(a.dataset.go,true);}));
show((location.hash||'').replace('#','')||ids[0],false);
window.addEventListener('hashchange',()=>show((location.hash||'').replace('#',''),false));
document.querySelectorAll('tr.jump').forEach(row=>{
  const go=()=>{const tgt=row.dataset.target;
    if(ids.includes(tgt)){show(tgt,true);return;}
    const el=document.getElementById(tgt);if(!el)return;el.scrollIntoView({behavior:'smooth',block:'start'});el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash');};
  row.addEventListener('click',go);
  row.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});
});
document.querySelectorAll('.copy-btn').forEach(btn=>{
  btn.addEventListener('click',()=>{
    const code=btn.closest('.code').querySelector('code').innerText;
    const done=()=>{btn.classList.add('done');const o=btn.textContent;btn.textContent='복사됨';setTimeout(()=>{btn.textContent=o;btn.classList.remove('done');},1500);};
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(code).then(done).catch(()=>{});}
    else{const ta=document.createElement('textarea');ta.value=code;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');}catch(e){}document.body.removeChild(ta);done();}
  });
});
document.querySelectorAll('.xref').forEach(a=>{
  a.addEventListener('click',e=>{e.preventDefault();const el=document.getElementById(a.dataset.target);if(!el)return;el.scrollIntoView({behavior:'smooth',block:'start'});el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash');});
});
const tt=document.getElementById('tt');
tt.addEventListener('click',()=>{const c=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';document.documentElement.setAttribute('data-theme',c);try{localStorage.setItem('a365theme',c);}catch(e){}});
</script>
</body>
</html>"""

PORTALS = [
 ("Copilot Studio", "에이전트 생성 · 지침/지식/도구 구성 · 게시", "https://copilotstudio.microsoft.com"),
 ("Microsoft 365 관리 센터 (MAC)", "에이전트 승인 · 전사 배포 · 인벤토리(레지스트리)", "https://admin.microsoft.com"),
 ("Microsoft Entra 관리 센터", "역할 할당 · 조건부 액세스 · 로그인 로그 · Gen AI 인사이트", "https://entra.microsoft.com"),
 ("Power Platform 관리 센터 (PPAC)", "환경 보안 · 위협 탐지 · 에이전트용 전역 보안 액세스(GSA)", "https://admin.powerplatform.microsoft.com"),
 ("Microsoft Defender 포털", "AI 보안 커넥터 · Copilot Studio 런타임 보호 정책", "https://security.microsoft.com"),
 ("Microsoft Purview 포털", "내부 위험 관리(IRM) · 감사 · 에이전트 리스크 경고", "https://purview.microsoft.com"),
]
ROLES = [
 ("0", "에이전트 생성", "환경 제작자(Maker) 이상", "Power Platform 관리 센터 · 환경/보안 역할"),
 ("1", "승인 및 전사 배포", "AI 관리자", "Entra > 사용자 > 할당된 역할"),
 ("2", "인벤토리 확인", "AI 읽기 권한자", "Entra > 사용자 > 할당된 역할"),
 ("3", "에이전트 차단", "AI 관리자 · 에이전트 ID 관리자", "Entra > 사용자 > 할당된 역할"),
 ("4", "조건부 접근제어", "조건부 액세스 관리자", "Entra > 사용자 > 할당된 역할"),
 ("5", "리스크 탐지", "내부자 위험 관리 분석가 또는 조사자", "Purview > 역할 및 범위 > 역할 그룹"),
 ("6", "런타임 보호", "애플리케이션 관리자 · 보안 관리자 · Power Platform 관리자", "Entra > 역할 / Power Platform 관리 센터"),
 ("7", "트래픽 모니터링", "전역 보안 액세스 관리자", "Entra > 사용자 > 할당된 역할"),
]

portal_rows = "".join(
    f'<tr><td class="pname">{esc(nm)}</td><td>{esc(desc)}</td>'
    f'<td><a class="portal-link" href="{url}" target="_blank" rel="noopener">{url.replace("https://","")} ↗</a></td></tr>'
    for nm, desc, url in PORTALS)
role_rows = "".join(
    f'<tr class="jump" data-target="{CH[int(num)]["id"]}" tabindex="0">'
    f'<td>{num}</td><td>{esc(step)}</td><td>{esc(role)}</td><td>{esc(loc)}</td></tr>'
    for num, step, role, loc in ROLES)

overview = f"""
  <section id="overview" class="page">
    <div class="hero">
      <span class="tag">Microsoft Agent 365 · Copilot Studio</span>
      <h1>Copilot Studio 에이전트</h1>
      <p>Copilot Studio(New experience)에서 만든 에이전트를 안전하게 운영하기 위한 <b>기본 보안 설정</b>을 처음부터 끝까지 안내합니다. 에이전트 생성 → 승인·배포 → 인벤토리 → 차단 → 조건부 접근제어 → 리스크 탐지 → 런타임 보호 → 트래픽 모니터링까지, 각 단계에서 어떤 포털에 들어가 무엇을 설정하는지 스크린샷과 함께 순서대로 짚어 드립니다.</p>
    </div>
    <p class="page-lead">이 가이드는 하나의 실습 환경에서 만든 데모 에이전트(<code>Agent365-Guide-Demo</code>)를 대상으로, 관리자·보안 담당자가 실제로 수행하는 구성 흐름을 재현합니다. 왼쪽 <b>구성 단계(0–7)</b> 목차에서 각 장으로 이동하고, 아래 표의 역할 행을 클릭하면 해당 단계로 바로 이동합니다.</p>

    <h2 class="ov-h">이 가이드의 범위 · Copilot Studio 참고</h2>
    <div class="scope-box">
      <p>본 가이드는 <b>Microsoft Agent 365의 관리·보안 기능</b>을 메인으로 다룹니다. 따라서 아래 <b>0. 에이전트 생성</b> 장은 실습에 필요한 최소한의 Copilot Studio 에이전트 생성 흐름만 담고 있습니다.</p>
      <p>지침 설계, 지식·도구(MCP) 심화 구성, 오케스트레이션, 채널·게시 등 <b>Copilot Studio 자체에 대한 더 자세한 내용</b>은 아래 문서를 참고하세요.</p>
      <a class="cta-link" href="https://chichoi1991.github.io/Agent_Blog/chapters/newcs0-overview/" target="_blank" rel="noopener">New Copilot Studio 핸즈온 가이드 바로가기 ↗</a>
    </div>

    <h2 class="ov-h">주요 진입 포털</h2>
    <p class="ov-sub">각 단계에서 사용하는 관리 포털입니다. 링크를 누르면 새 탭에서 해당 포털이 열립니다. 실제 접근에는 아래 <b>필요한 역할</b>이 선행되어야 합니다.</p>
    <div class="tw"><table><thead><tr><th>포털</th><th>이 가이드에서의 용도</th><th>바로가기</th></tr></thead><tbody>{portal_rows}</tbody></table></div>

    <h2 class="ov-h">단계별 필요한 역할 한눈에</h2>
    <p class="ov-sub">각 단계를 수행하기 전에 아래 역할을 미리 할당해 두세요. 대부분 <b>Entra 관리 센터 &gt; 사용자 &gt; 할당된 역할 &gt; 할당 추가</b>에서 부여하며, 5장은 Purview 역할 그룹, 6장 일부는 Power Platform 관리자 지정이 필요합니다. 행을 클릭하면 해당 단계로 이동합니다.</p>
    <div class="tw"><table><thead><tr><th>#</th><th>단계</th><th>필요한 역할</th><th>할당 위치</th></tr></thead><tbody>{role_rows}</tbody></table></div>
    <div class="note">역할은 <b>최소 권한 원칙</b>에 따라 필요한 단계에만 부여하고, 실습이 끝나면 회수하는 것을 권장합니다. AI 관리자·에이전트 ID 관리자·조건부 액세스 관리자 등은 테넌트 전체에 영향을 주는 상위 권한이므로 할당 대상을 신중히 관리하세요.</div>

    <h2 class="ov-h">0단계를 건너뛰고 바로 시작하기 · 에이전트 Import</h2>
    <p class="ov-sub"><b>0. 에이전트 생성</b>을 건너뛰고 준비된 실습용 에이전트로 곧바로 Agent 365 기능(1~7단계)을 실습하려면, 아래 앱 패키지를 Teams에 업로드하세요. 두 가지 방법으로 사용할 수 있습니다.</p>
    <a class="download-btn" href="files/Agent365-Guide-Demo.zip" download>⬇ 실습용 에이전트 패키지 내려받기 (Agent365-Guide-Demo.zip)</a>
    <div class="method">
      <div class="method-head"><span class="method-no">1</span> 나 / 소수만 테스트 — 사이드로드</div>
      <p>Teams → <b>앱</b> → <b>앱 관리</b> → <b>앱 업로드</b> → <b>사용자 지정 앱 업로드</b>에 zip을 그대로 올립니다.</p>
      <p class="method-cond">※ 테넌트에서 <b>사용자 지정 앱 업로드(사이드로드)</b>가 허용되어 있어야 합니다.</p>
    </div>
    <div class="method">
      <div class="method-head"><span class="method-no">2</span> 조직 전체에 배포 — Teams 관리 센터</div>
      <p><a href="https://admin.teams.microsoft.com" target="_blank" rel="noopener">admin.teams.microsoft.com</a> → <b>Teams 앱</b> → <b>앱 관리</b> → <b>새 앱 업로드</b> → zip 업로드 → 해당 앱을 <b>앱 설정 정책</b>에 추가해 사용자/그룹에게 배포합니다.</p>
      <p class="method-cond">M365 Copilot에서도 같은 앱이 에이전트로 노출됩니다.</p>
    </div>

    <div class="pagenav"><span class="pn-empty"></span><a class="nxt" href="#ch0" data-go="ch0"><span class="lbl">다음 →</span><br>0. 에이전트 생성</a></div>
  </section>"""
parts.insert(0, overview)

nav_html = "\n    ".join(
    f'<a href="#{c["id"]}" data-sec="{c["id"]}" class="nav-sub"><span class="n">{c["num"]}</span><span>{esc(c["name"])}</span></a>'
    for c in CH)
out = HTML.replace("__CSS__", CSS).replace("__NAV__", nav_html).replace("__SECTIONS__", "\n".join(parts))
path = os.path.join(BASE, "index.html")
open(path, "w", encoding="utf-8").write(out)
print("written", len(out))
