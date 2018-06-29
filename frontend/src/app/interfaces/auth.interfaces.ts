// Log in credentials
export interface Credentials {
    // Just texts
    username: string;
    password: string;
}

// Change Password Credentials
export interface Password {
    // Just texts
    oldPassword: string;
    newPassword: string;
    repeatNewPassword: string;
}
