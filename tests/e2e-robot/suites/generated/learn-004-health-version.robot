*** Settings ***
Documentation    AUTO-GENERATED — ticket learn-004
...              REVIEW REQUIRED before merge (Bước D)
...              API E2E: GET /health includes version (LEARN-003)
Resource           ../../resources/api_keywords.robot
Variables          ../../variables/env/local.yaml
Suite Setup        API Session Is Ready
Force Tags         generated    learn-004

*** Test Cases ***
Health Returns API Version
    [Tags]    generated    learn-004    smoke
    ${resp}=    GET On Session    app    /health    expected_status=200
    Should Be Equal As Strings    ${resp.json()}[status]    ok
    Should Be Equal As Strings    ${resp.json()}[service]    workflow-ai-poc
    Should Be Equal As Strings    ${resp.json()}[version]    0.2.0
