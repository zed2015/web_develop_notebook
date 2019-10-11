#### BcryptPasswordEncoder
- BcryptPasswordEncode(strength 12)
- .encode(rawPassword)
    - randomSalt = BCrpyt.genSalt(stregnth)
    - BCrypt.hashpw(rawPassword,randomSalt)
        - salt + hash
        - base64
- matches(rawPassword,password)
    - Bcrypt.checkpw(rawPassword,password)
        - hashedPassword = Bcrypt.hashpw(rawPassword,password)
        - hashedPassword.equal(password)

