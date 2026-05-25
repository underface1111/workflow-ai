*** Settings ***
Library    RequestsLibrary

*** Variables ***
${AUTH_TOKEN}    ${EMPTY}

*** Keywords ***
API Session Is Ready
    Create Session    app    ${BASE_URL}    verify=${False}

Login As Demo User
    ${resp}=    POST On Session    app    /auth/login
    ...    json={"email": "${TEST_EMAIL}", "password": "${TEST_PASSWORD}"}
    ...    expected_status=200
    ${token}=    Set Variable    ${resp.json()}[token]
    Set Suite Variable    ${AUTH_TOKEN}    ${token}

Authorized GET
    [Arguments]    ${path}    ${expected_status}=200
    ${headers}=    Create Dictionary    Authorization=Bearer ${AUTH_TOKEN}
    ${resp}=    GET On Session    app    ${path}    headers=${headers}    expected_status=${expected_status}
    RETURN    ${resp}

Authorized POST
    [Arguments]    ${path}    ${body}=${EMPTY}    ${expected_status}=200
    ${headers}=    Create Dictionary    Authorization=Bearer ${AUTH_TOKEN}
    IF    '${body}' == '${EMPTY}'
        ${resp}=    POST On Session    app    ${path}    headers=${headers}    expected_status=${expected_status}
    ELSE
        ${resp}=    POST On Session    app    ${path}    json=${body}    headers=${headers}    expected_status=${expected_status}
    END
    RETURN    ${resp}
