*** Settings ***
Documentation    Steel thread E2E (API): login → catalog → cart → checkout
...              Tags: critical — run on PR per ADR-03
Library            Collections
Resource           ../../resources/api_keywords.robot
Variables          ../../variables/env/local.yaml
Suite Setup        API Session Is Ready

*** Test Cases ***
Health Check Is Available
    [Tags]    critical    smoke
    ${resp}=    GET On Session    app    /health    expected_status=200
    Should Be Equal As Strings    ${resp.json()}[status]    ok

Steel Thread Happy Path Checkout
    [Tags]    critical    steel-thread
    Login As Demo User
    ${catalog}=    Authorized GET    /catalog
    Length Should Be    ${catalog.json()}[items]    2
    ${cart_payload}=    Create Dictionary    skuId=sku-2    quantity=${1}
    ${add}=    Authorized POST    /cart/items    ${cart_payload}    201
    ${checkout}=    Authorized POST    /checkout
    Should Be Equal As Strings    ${checkout.json()}[status]    confirmed
    Should Match Regexp    ${checkout.json()}[orderId]    ^ord-
