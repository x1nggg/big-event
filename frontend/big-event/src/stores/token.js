//定义store

import { defineStore } from "pinia";
import { ref } from 'vue'
/*
 第一个参数 名字
第二个参数   函数
第三个参数  
*/
export const useTokenStore = defineStore('token',()=>{
    //响应式变量
    const token = ref('')
    //定义函数修改token的值
    const setToken = (newToken)=>{
        token.value= newToken;
    }

    //移除token函数
    const removeToken = ()=>{
        token.value='';
    }
    

    return{
        token,setToken,removeToken
    }
},{
    persist:true  //持久化存储，防止刷新刷掉token
});