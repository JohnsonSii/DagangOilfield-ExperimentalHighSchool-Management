<template>
  <!-- 上传成功提示框 -->
  <uni-popup ref="alertDialog" type="dialog">
    <uni-popup-dialog type="info" cancelText="关闭" confirmText="同意" title="上传成功" content="待管理员审核完成后将于下方展示入群二维码，请及时关注。"></uni-popup-dialog>
  </uni-popup>

  <!-- 隐私提示框 -->
  <uni-popup ref="alertDialogProtect" type="dialog">
    <uni-popup-dialog type="info" cancelText="关闭" confirmText="同意" title="隐私保护声明" :content="protectText" @confirm="dialogConfirm"></uni-popup-dialog>
  </uni-popup>

  <!-- 加载蒙版 -->
  <view class="mask center" v-show="loading">
    <uni-load-more status="loading" iconType="circle" color="#444" :iconSize="50" :showText="false"></uni-load-more>
  </view>

  <!-- 页面可见元素 -->
  <view class="container">
    <!-- 导航栏 -->
    <view class="header flexr fab sac whitefont smallshadow" :style="headerStyle">
      <view class="center" style="width: 100rpx" @click="handleBack">
        <uni-icons type="undo-filled" color="white" size="26"></uni-icons>
      </view>
      <view class="custom-title f1 center">提交审核材料</view>
      <view class="center" style="width: 100rpx" @click="handleMagic">
        <uni-icons type="smallcircle" color="white" size="26"></uni-icons>
      </view>
    </view>

    <!-- 文档流占位元素 -->
    <view class="fake-header"></view>

    <!-- 正文 -->
    <view class="content coll">
      <!-- 表单 -->
      <view class="boom mt2 mb2">
        <uni-forms ref="baseForm" :modelValue="baseFormData">
          <uni-forms-item label="姓名" required>
            <uni-easyinput v-model="baseFormData.name" placeholder="请输入姓名" maxlength="10" />
          </uni-forms-item>
          <uni-forms-item label="学校" required>
            <uni-easyinput v-model="baseFormData.school" placeholder="请输入初中毕业学校" maxlength="20" />
          </uni-forms-item>
          <uni-forms-item label="QQ号" required>
            <uni-easyinput v-model="baseFormData.qq" placeholder="请输入QQ号" maxlength="20" />
          </uni-forms-item>
          <uni-forms-item required>
            <uni-file-picker ref="files" :auto-upload="false" limit="1" title="请上传录取通知书照片"></uni-file-picker>
          </uni-forms-item>
        </uni-forms>

        <view class="mb2 rowl">
          <checkbox style="transform: scale(0.8)" color="#3D71FF" :checked="checkBoxChecked" @click="handleCheckbox" />
          <text class="midfont" @click="handleTipOfProtect">隐私保护声明</text>
        </view>
        <button type="primary" @click="submit('baseForm')" style="background-color: #3d71ff; border-radius: 50rpx">提交</button>
      </view>
      <!-- 表单结束 -->

      <!-- 图像 -->
      <view class="smallfont mt text">{{ tipFirst }}</view>

      <view class="smallfont mt warntext" v-if="imgShow">{{ tipSecond }}</view>

      <view class="" v-if="imgShow">
        {{ textTip }}
      </view>

      <view class="canvas center bigradius">
        <image v-if="imgShow" :src="imgUrl" mode="aspectFill" @tap="_previewImage(imgUrl)"></image>
        <image v-if="!imgShow && passed == 0" src="/static/img/qrcode.jpg" mode="aspectFill" @click="handleFreshPassed"></image>
      </view>

      <!-- 图像结束 -->
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      imgShow: false,
      imgUrl: '',
      protectText: '',
      tipFirst: '',
      tipSecond: '',
      loading: false,
      headerStyle: {
        height: '100rpx',
        width: '100%',
        borderBottomLeftRadius: '20rpx',
        borderBottomRightRadius: '20rpx',
        borderTopLeftRadius: '0',
        borderTopRightRadius: '0',
        top: '0',
        left: '0',
        background: 'rgba(0, 95, 255, 0.8)'
      },
      baseFormData: {
        name: '',
        school: '',
        qq: ''
      },
      checkBoxChecked: false,
      username: '',
      role: 0,
      passed: 0,
      id: ''
    };
  },
  methods: {
    // 功能函数

    // 预览图片
    _previewImage(image) {
      var imgArr = [];
      imgArr.push(image);
      uni.previewImage({
        urls: imgArr,
        current: imgArr[0]
      });
    },

    // 请求二维码
    requestQRCode() {
      if (this.passed == 1) {
        this.imgShow = true;
        uni.request({
          url: 'https://apis.johnsonsii.cn/apis/getqrcode/',
          method: 'GET',
          responseType: 'arraybuffer',
          success: (res) => {
            const base64 = uni.arrayBufferToBase64(res.data);
            this.imgUrl = 'data:image/jpeg;base64,' + base64; // 将图片数据转换为 Base64 格式
            this.textTip = '';
          },
          fail: (err) => {
            console.error(err);
          }
        });
      } else {
        this.imgShow = false;
      }
    },

    // 绑定函数

    handleFreshPassed() {
      this.loading = true;
      setTimeout(() => {
        uni.request({
          url: `https://apis.johnsonsii.cn/apis/getuserinfo?username=${this.username}`,
          success: (res) => {
            this.loading = false;
            this.passed = res.data.passed;
            this.requestQRCode();
          }
        });
      }, 1000);
    },

    // 导航栏事件
    handleBack() {
      uni.navigateBack();
    },
    // 导航栏动画
    handleMagic() {
      this.headerStyle.height = this.headerStyle.height === '100rpx' ? '90rpx' : '100rpx';
      this.headerStyle.width = this.headerStyle.width === '100%' ? '95%' : '100%';
      this.headerStyle.borderTopLeftRadius = this.headerStyle.borderTopLeftRadius === '0' ? '30rpx' : '0';
      this.headerStyle.borderTopRightRadius = this.headerStyle.borderTopRightRadius === '0' ? '30rpx' : '0';
      this.headerStyle.borderBottomLeftRadius = this.headerStyle.borderBottomLeftRadius === '20rpx' ? '30rpx' : '20rpx';
      this.headerStyle.borderBottomRightRadius = this.headerStyle.borderBottomRightRadius === '20rpx' ? '30rpx' : '20rpx';
      this.headerStyle.top = this.headerStyle.top === '0' ? '10rpx' : '0';
      this.headerStyle.left = this.headerStyle.left === '0' ? 'calc(0.025 * 100vw)' : '0';
    },
    // 选择框事件
    handleCheckbox() {
      this.checkBoxChecked = this.checkBoxChecked === false ? true : false;
    },
    // 隐私保护声明事件
    handleTipOfProtect() {
      this.$refs.alertDialogProtect.open();
    },
    // 对话框事件
    dialogConfirm() {
      this.checkBoxChecked = true;
    },

    // 提交表单事件
    submit(ref) {
      const fileList = this.$refs.files.files;
      // 如果有文件
      if (fileList.length > 0 && this.baseFormData.name != '' && this.baseFormData.school != '' && this.baseFormData.qq != '') {
        if (this.checkBoxChecked === false) {
          this.$refs.alertDialogProtect.open();
          return;
        }
        this.loading = true;
        // 获取第一个文件
        const file = fileList[0];

        uni.uploadFile({
          url: 'https://apis.johnsonsii.cn/apis/receive/',
          filePath: file.path,
          name: 'file',
          formData: {
            name: this.baseFormData.name,
            school: this.baseFormData.school,
            qq: this.baseFormData.qq,
            id: this.id,
            username: this.username,
            passed: this.passed
          },
          success: (res) => {
            this.loading = false;
            console.log(res.data);
            this.$refs.alertDialog.open();
            if (this.passed === 2) {
              uni.request({
                url: `https://apis.johnsonsii.cn/apis/setuserpassed?username=${this.username}&passed=0`,
                success: (res) => {
                  this.passed = 0;
                }
              });
            }
          },
          fail: (err) => {
            this.loading = false;
            uni.showToast({
              title: '上传失败，请压缩图片尺寸后重试',
              icon: 'none'
            });
          }
        });
      } else {
        this.loading = false;
        uni.showToast({
          title: '信息填写不完整',
          icon: 'none'
        });
      }
    }
  },
  onLoad(option) {
    this.username = option.username;
    uni.request({
      url: `https://apis.johnsonsii.cn/apis/getuserinfo?username=${this.username}`,
      success: (res) => {
        this.role = res.data.role;
        this.passed = res.data.passed;
        this.id = res.data.id;
        this.requestQRCode();
      }
    });
    uni.request({
      url: '/static/json/index.json',
      success: (res) => {
        this.protectText = res.data.protectText;
        this.tipFirst = res.data.tipFirst;
        this.tipSecond = res.data.tipSecond;
      }
    });
  }
};
</script>

<style>
@import '../../static/css/global.scss';

.container {
  width: 100%;
  max-width: 768px;
  margin: 0 auto;
}

.content {
  width: 85%;
  margin: 0 auto;
}
/* 导航栏样式 */
.header {
  box-sizing: border-box;
  position: fixed;
  padding: 0 5rpx;
  z-index: 2000;
  backdrop-filter: blur(10rpx);
  transition: 0.5s all;
}
.fake-header {
  position: relative;
  pointer-events: none;
  height: 100rpx;
}
.mask {
  position: fixed;
  height: 100%;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 8000;
}
.canvas {
  width: 80%;
  height: calc(0.65 * 100vw);
  border: 1px dashed gray;
  overflow: hidden;
  margin: 50rpx auto;
}
.canvas image {
  width: 85%;
  height: 85%;
  border-radius: 35rpx;
}
</style>
