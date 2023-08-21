<template>
  <!-- 弹窗提醒 -->
  <view>
    <!-- 注册弹窗 -->
    <uni-popup ref="registerPopup" background-color="#fff">
      <view class="register-content coll">
        <text class="text mb2">该用户尚未注册，请注册后登录</text>
        <view class="imptext hugefont mb">注册</view>
        <uni-easyinput v-model="registerPassword" placeholder="请输入密码" type="password" maxlength="16" />
        <uni-easyinput v-model="registerValidatePassword" placeholder="请重复密码" type="password" maxlength="16" @input="handleRigesterInput" />
        <view v-if="registerPasswordWarning" class="warntext smallfont mb">*两次输入的密码不一致</view>
        <button class="register-button midfont whitefont center" @click="handleRigester">注册并登录</button>
      </view>
    </uni-popup>
  </view>

  <view>
    <!-- 登录弹窗 -->
    <uni-popup ref="loginPopup" background-color="#fff">
      <view class="login-content coll">
        <text class="text mb2">请输入密码</text>
        <view class="imptext hugefont mb2">登录</view>
        <uni-easyinput v-model="loginPassword" placeholder="请输入密码" type="password" maxlength="16" @input="handleLoginComfirmInput" />
        <button class="register-button midfont whitefont center" @click="handleLoginConfirm">确认登录</button>
      </view>
    </uni-popup>
  </view>

  <!-- 加载蒙版 -->
  <view class="mask center" v-show="loading">
    <uni-load-more status="loading" iconType="circle" color="#444" :iconSize="50" :showText="false"></uni-load-more>
  </view>

  <!-- 页面可见元素 -->
  <view class="container colc">
    <!-- 背景图片 -->
    <view class="bg-card midshadow midradius">
      <image class="boom" src="/static/img/bg.jpg" mode="aspectFill"></image>
    </view>

    <!-- 正文部分 -->
    <view class="article mt2 mb2 coll">
      <view class="title">
        {{ jsonData.title }}
      </view>
      <view class="subtitle rowl mt">
        <view>{{ jsonData.subtitleFirst }}</view>
        <view class="imptext ml-1">{{ jsonData.subtitleSecond }}</view>
      </view>
      <view class="text mt">
        {{ jsonData.text }}
      </view>
    </view>

    <!-- 登录控制器 -->
    <view class="controller mb2">
      <!-- 手机号输入框 -->
      <view class="phone-input">
        <view class="input-component center" @click="handleInputComponent">
          <uni-icons v-if="clearing" type="clear" size="25" color="gray"></uni-icons>
        </view>
        <input class="specific-size custom-input smallshadow rowl" v-model="phoneNumber" type="tel" placeholder="请输入手机号" maxlength="11" @input="handleLoginInput" />
      </view>
      <!-- 快捷登录按钮 -->
      <button class="specific-size custom-button smallshadow whitefont mt2 center" @click="handleLogin">
        <uni-icons class="mr-1" type="paperplane-filled" size="20" color="white"></uni-icons>
        快捷登录
      </button>
    </view>
  </view>
</template>

<script>
import md5 from 'js-md5';
export default {
  data() {
    return {
      loginPassword: '',
      registerPassword: '',
      registerValidatePassword: '',
      registerPasswordWarning: false,
      loading: false,
      phoneNumber: '',
      clearing: false,
      jsonData: {},
      role: 0
    };
  },
  methods: {
    // 键盘监听
    handleLoginInput(event) {
      if (event.keyCode === 13) {
        this.handleLogin();
      }
    },
    handleRigesterInput(event) {
      if (event.keyCode === 13) {
        this.handleRigester();
      }
    },
    handleLoginComfirmInput(event) {
      if (event.keyCode === 13) {
        this.handleLoginConfirm();
      }
    },

    // 功能函数
    validatePhoneNumber(phoneNumber) {
      const phoneNumberRegex = /^1[0-9]{10}$/;
      return phoneNumberRegex.test(this.phoneNumber);
    },

    // 绑定函数

    // 注册
    handleRigester() {
      if (this.registerPassword === '') {
        uni.showToast({
          title: '密码不能为空',
          icon: 'none'
        });
        return
      }
      if (this.registerPasswordWarning === false) {
        const username = this.phoneNumber;
        const password = md5(this.registerPassword);
        this.loading = true;
        uni.request({
          url: 'https://apis.johnsonsii.cn/apis/register/',
          method: 'POST',
          data: {
            username: username,
            password: password
          },
          header: {
            'content-type': 'application/x-www-form-urlencoded'
          },
          success: (res) => {
            this.loading = false;
            this.$refs.registerPopup.close();
            this.loginPassword = this.registerPassword;
            this.handleLoginConfirm();
          }
        });
      } else {
        uni.showToast({
          title: '密码不一致',
          icon: 'none'
        });
      }
    },

    // 登录确认
    handleLoginConfirm() {
      const username = this.phoneNumber;
      const password = md5(this.loginPassword);
      this.loading = true;
      uni.request({
        url: 'https://apis.johnsonsii.cn/apis/login/',
        method: 'POST',
        data: {
          username: username,
          password: password
        },
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        },
        success: (res) => {
          this.loading = false;
          if (res.data === 0) {
            uni.showToast({
              title: '密码错误',
              icon: 'error'
            });
          } else {
            this.role = res.data.role;
            this.$refs.loginPopup.close();
            if (this.role === 0) {
              uni.navigateTo({
                url: `/pages/index/index?username=${username}`
              });
            } else {
              uni.navigateTo({
                url: `/pages/admin/admin?username=${username}`
              });
            }
          }
        }
      });
    },
    handleInputComponent() {
      this.phoneNumber = '';
    },

    // 快捷登录
    handleLogin() {
      // const self = this;

      if (this.validatePhoneNumber(this.phoneNumber) === false) {
        uni.showToast({
          title: '手机号验证失败',
          icon: 'none'
        });
        return;
      }

      this.loading = true;
      uni.request({
        url: `https://apis.johnsonsii.cn/apis/validateuserexist?username=${this.phoneNumber}`,
        method: 'GET',
        success: (res) => {
          this.loading = false;
          if (res.data === 0) {
            console.log('register');
            this.$refs.registerPopup.open('bottom');
          } else {
            this.$refs.loginPopup.open('bottom');
          }
        }
      });
    }
  },
  onLoad() {
    uni.request({
      url: '/static/json/login.json',
      success: (res) => {
        this.jsonData = res.data;
      }
    });
  },
  watch: {
    phoneNumber(newVal) {
      this.clearing = this.phoneNumber === '' ? false : true;
    },
    registerValidatePassword(newVal) {
      this.registerPasswordWarning = this.registerPassword === this.registerValidatePassword ? false : true;
    }
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

.bg-card {
  width: 92%;
  height: 450rpx;
  overflow: hidden;
  margin-top: 32rpx;
}

.article {
  width: 92%;
}

.controller {
  width: 85%;
  margin-top: 80rpx;
}

.custom-input {
  background-color: rgba(100, 100, 100, 0.1);
  padding: 20rpx 40rpx;
  margin: auto;
  font-size: 30rpx;
  z-index: 1;
}

.custom-button {
  background-color: #00c777;
  font-size: 30rpx;
}

.specific-size {
  width: 100%;
  box-sizing: border-box;
  height: 90rpx;
  border-radius: 50rpx;
}

.phone-input {
  position: relative;
}

.input-component {
  position: absolute;
  width: 90rpx;
  height: 90rpx;
  right: 20rpx;
  z-index: 2;
}
.mask {
  position: fixed;
  height: 100%;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 8000;
}
.register-content {
  box-sizing: border-box;
  height: 550rpx;
  padding: 30rpx;
}
.register-button {
  width: 100%;
  border-radius: 50rpx;
  background-color: rgba(0, 95, 255, 0.8);
  height: 90rpx;
}
.login-content {
  box-sizing: border-box;
  height: 450rpx;
  padding: 30rpx;
}
</style>
