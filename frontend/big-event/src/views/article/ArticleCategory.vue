<script setup>
import {
    Edit,
    Delete
} from '@element-plus/icons-vue'
//增加加载属性
const loading = ref(false);
//自定义加载图像
const svg = `
          <path class="path" d="
            M 30 15
            L 28 17
            M 25.61 25.61
            A 15 15, 0, 0, 1, 15 30
            A 15 15, 0, 1, 1, 27.99 7.5
            L 15 15
          " style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"/>
        `
import { ref } from 'vue'
const categorys = ref([
    {
        "id": '',
        "categoryName": '',
        "categoryAlias": '',
        "createTime": '',
        "updateTime": ''
    }
])
//声明一个异步函数
import {articleCategoryListService,articleCategoryAddService,articleCategoryUpdateService,articleCategoryDeleteService} from '@/api/article.js'

//渲染数据
const articleCategoryList= async()=>{
    loading.value = true;
    let result = await articleCategoryListService();
    categorys.value =  result.data;
    loading.value = false;
}
articleCategoryList();



//控制添加分类弹窗
const dialogVisible = ref(false)

//添加分类数据模型
const categoryModel = ref({
    categoryName: '',
    categoryAlias: ''
})
//添加分类表单校验
const rules = {
    categoryName: [
        { required: true, message: '请输入分类名称', trigger: 'blur' },
    ],
    categoryAlias: [
        { required: true, message: '请输入分类别名', trigger: 'blur' },
    ]
}

//调用api，添加表单
import { ElMessage,ElMessageBox } from 'element-plus';
const addCategory=async()=>{
    let result = await articleCategoryAddService(categoryModel.value);
    ElMessage.success(result.msg? result.msg: '添加成功');

    //调用获取文章分类的函数
    articleCategoryList();
    //消除弹窗
    dialogVisible.value=false;
}
//定义变量，控制弹窗标题的显示
const title = ref('');
//展示编辑弹窗
const showDialog = (row)=>{
    dialogVisible.value=true;
    title.value='编辑分类';
    //数据拷贝
    categoryModel.value.categoryName=row.categoryName;
    categoryModel.value.categoryAlias=row.categoryAlias;
    //扩展id属性传递给后台进行修改
    categoryModel.value.id = row.id;
    
}
//修改文章分类
const updateCategory=async()=>{
   //调用接口
   let result = await articleCategoryUpdateService(categoryModel.value);

   ElMessage.success(result.msg? result.msg: '修改成功');
   //调用获取文章分类的函数
   articleCategoryList();
    //消除弹窗
   dialogVisible.value=false;
}

//清空模型数据
const clearData = ()=>{
    categoryModel.value.categoryAlias='';
    categoryModel.value.categoryName='';
}
//删除分类
const deleteCategory = (row)=>{

    ElMessageBox.confirm(
    '你确认要删除该分类信息吗?',
    '温馨提示',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async() => {
        //调用接口
       let result = await articleCategoryDeleteService(row.id);
      ElMessage({
        type: 'success',
        message: '删除成功',
      })
      //刷新列表
      articleCategoryList();
    })
    .catch(() => {
      ElMessage({
        type: 'success',
        message: '取消删除',
      })
    })
}
</script>
<template>
    <el-card class="page-container">
        <template #header>
            <div class="header">
                <span>文章分类</span>
                <div class="extra">
                    <el-button type="primary" @click="dialogVisible=true;title='添加分类';clearData()">添加分类</el-button>
                </div>
            </div>
        </template>
        <el-table :data="categorys" style="width: 100%" v-loading="loading" :element-loading-svg="svg" class="custom-loading-svg">
            <el-table-column label="序号" width="100" type="index"> </el-table-column>
            <el-table-column label="分类名称" prop="categoryName"></el-table-column>
            <el-table-column label="分类别名" prop="categoryAlias"></el-table-column>
            <el-table-column label="操作" width="100">
                <template #default="{ row }">
                    <el-button :icon="Edit" circle plain type="primary" @click="showDialog(row)"></el-button>
                    <el-button :icon="Delete" circle plain type="danger" @click="deleteCategory(row)"></el-button>
                </template>
            </el-table-column>
            <template #empty>
                <el-empty description="没有数据" />
            </template>
        </el-table>

        <!-- 添加分类弹窗 -->
         <el-dialog v-model="dialogVisible" :title=title width="30%">
            <el-form :model="categoryModel" :rules="rules" label-width="100px" style="padding-right: 30px">
                <el-form-item label="分类名称" prop="categoryName">
                    <el-input v-model="categoryModel.categoryName" minlength="1" maxlength="10"></el-input>
                </el-form-item>

                <el-form-item label="分类别名" prop="categoryAlias">
                     <el-input v-model="categoryModel.categoryAlias" minlength="1" maxlength="15"></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="title==='添加分类'? addCategory() : updateCategory()"> 确认 </el-button>
                 </span>
            </template>
        </el-dialog>
    </el-card>
</template>

<style lang="scss" scoped>
//加载样式
.example-showcase .el-loading-mask {
    z-index: 9;
}
.page-container {
    min-height: 100%;
    box-sizing: border-box;

    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
}
</style>
