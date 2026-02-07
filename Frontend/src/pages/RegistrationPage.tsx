export const RegistrationPage = () => {
  return (
    <div>
        {/* This is a registration page */}
        <form action="" method="post">
            <label htmlFor="">Username</label>
            <input type="text" placeholder="Abebe_aslask" /><br />
            <label htmlFor="">Email</label>
            <input type="text" placeholder="Abebe@gmail.com" /><br />
            <label htmlFor="">Password</label>
            <input type="password" placeholder="Enter Password " /><br />

            <input type="submit" value={"Submit"} />
            
        </form>
    </div>
  )
}
