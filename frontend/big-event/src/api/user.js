//导入request.js请求工具
import request from '@/utils/request.js'

//提供调用注册接口的函数
export const userRegisterService =(registerData)=>{
     return request.post('/user/register',registerData);
}


//提供调用登录接口的函数
export const userLoginService=(loginData)=>{
      return request.post('/user/login',loginData);
}

//获取用户详细信息
export const userInfoService=()=>{
   return request.get('/user/userinfo');
}

//修改个人信息

export const userInfoUpdateService=(userInfoData)=>{
   return request.put('/user/update',userInfoData)
}

//修改用户头像
export const userAvatarUpdateService=(avatarUrl)=>{
   return request.patch('/user/updateAvatar',{avatarUrl:avatarUrl});
}

//更新用户密码
export const userUpdatePwdService=(pwdData)=>{
   const params = {
      old_pwd: pwdData.oldPwd,
      new_pwd: pwdData.newPwd,
      re_pwd: pwdData.rePwd
   }
    return request.patch('/user/updatePwd',params);
}

//退出登录删除后台redis存储的token
export const userLogoutService=()=>{
    return request.post('/user/logout');
}