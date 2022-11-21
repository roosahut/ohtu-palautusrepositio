*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Register Page

*** Test Cases ***
Register With Valid Username And Password
    Set Username  rosis
    Set Password  salainen1
    Set Password Confirmation  salainen1
    Submit Credentials
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  ro
    Set Password  salainen1
    Set Password Confirmation  salainen1
    Submit Credentials
    Register Should Fail With Message  Username should be at least 3 characters

Register With Valid Username And Too Short Password
    Set Username  rosis
    Set Password  sala1
    Set Password Confirmation  sala1
    Submit Credentials
    Register Should Fail With Message  Password should be at least 8 characters

Register With Nonmatching Password And Password Confirmation
    Set Username  rosis
    Set Password  salainen1
    Set Password Confirmation  vääääärää1
    Submit Credentials
    Register Should Fail With Message  Passwords do not match

Login After Successful Registration
    Go To Login Page
    Set Username  rosis
    Set Password  salainen1
    Submit Credentials Login
    Login Should Succeed

Login After Failed Registration
    Go To Login Page
    Set Username  ro
    Set Password  salainen1
    Submit Credentials Login
    Login Should Fail With Message  Invalid username or password

*** Keywords ***
Register Should Succeed
    Title Should Be  Welcome to Ohtu Application!

Submit Credentials
    Click Button  Register

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Login Should Succeed
    Main Page Should Be Open

Login Should Fail With Message
    [Arguments]  ${message}
    Login Page Should Be Open
    Page Should Contain  ${message}

Submit Credentials Login
    Click Button  Login