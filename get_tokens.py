from amocrm.v2 import tokens

if __name__ == '__main__':  
    tokens.default_token_manager(
        client_id="adff957c-f828-4d10-8008-21f3e8781733",
        client_secret="er3tJARihFWuZMF8bneTqm6OF4jcOrYYwbsMMy6slYt4cWQbbk1H3T5L3jOCTvEM",
        subdomain="anvarjonsts",
        redirect_url="https://api.sts-shop.uz",
        storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
    )
    # tokens.default_token_manager.init(code="def5020014a6302a979ccde0ec6aa66908a343ee50e4d9f1cdeddacc544a2148638138738d0159069683152edfc5c89d20313942c0b75264044f8b83c11e14be1f75b95677e11499c5cc6c574a4d043b609c348be1df05e4f9e8eef7bc5426d2bc9ef5fbe11556b6645c3f02ec80ff4acda36bdb083eadd529004155d26b5a8c5a62461272023163ba288d3bb7ed12d21c63829d7bfe65559592c54945b590c51b56404202da22662eb270aac656a54126a342c459c48fb8f116374bb462b04ffefac9b9bba30a5975cfbdb8bff00ac8b8db9121c75025f84edc7d4e97fc89bb0d5cc7c5dddf0c8ead4804526e80371a9fcb67fd20e91e11334fff0ad375e99a0d4f4ba4c83779cba710a0c4d1ebaba9847f517fedf24ff57daa9046f2d07799171e0a67fb2700e44b46234cf3b911f10eb0afc30cb5be0f7370abc160bb83c725f74e146161b416bec43e1544cdca7f5d9692d4d6722db7f76e0dc44c5b41fb6d97f9233800aa2aa1f4cae66197d1dda7ee471866fe91860f5e06161896ac18cace19c56064599430adb1cf0284bcee0c264864670dc7e5ff40087acbefd775115e544f911d114ebc1460b8fc19b99d27af876471f88252f2c93e8b5921dc19c753ea38b22244ea8cd1d0054a540b202459053e0d05def4a22beaf2b5d285cc4754c28f265861fe", 
    #                                   skip_error=False)

    