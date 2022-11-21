*** Settings ***
Resource  resource.robot

*** Test Cases ***
Register With Valid Username And Password
    Input New Command
    Input Credentials  rosis  salainen123
    Output Should Contain  New user registered

Register With Already Taken Username And Valid Password
    Input New Command
    Input Credentials  rosis  salainen123
    Input New Command
    Input Credentials  rosis  salainensana111
    Output Should Contain  User with username rosis already exists

Register With Too Short Username And Valid Password
    Input New Command
    Input Credentials  r  salainen123
    Output Should Contain  Username should be at least 3 characters

Register With Valid Username And Too Short Password
    Input New Command
    Input Credentials  rosis  sala12
    Output Should Contain  Password should be at least 8 characters

Register With Valid Username And Long Enough Password Containing Only Letters
    Input New Command
    Input Credentials  rosis  salainensana
    Output Should Contain  Password is too simple