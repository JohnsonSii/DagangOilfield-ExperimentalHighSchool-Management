<template>
  <!-- 审核通过提示框 -->
  <uni-popup ref="alertDialog" type="dialog">
    <uni-popup-dialog type="info" cancelText="关闭" confirmText="同意" title="请确认" content="您是否同意通过该用户的审核。" @confirm="dialogConfirm"></uni-popup-dialog>
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
      <view class="f1 center">审核管理</view>
      <view class="center" style="width: 100rpx" @click="handleMagic">
        <uni-icons type="smallcircle" color="white" size="26"></uni-icons>
      </view>
    </view>

    <!-- 文档流占位元素 -->
    <view class="fake-header"></view>

    <!-- 正文 -->
    <view class="content colc">
      <view class="custom-title">身份卡</view>
      <view class="infocard col-left-top">
        <!-- 抬头 -->
        <view class="row-left" style="height: 25%; margin-top: 30rpx">
          <uni-icons type="contact" size="80"></uni-icons>
          <view class="col-left-around" style="height: 100%">
            <text style="font-size: 22rpx">联系电话：{{ username }}</text>
            <view class="row-left">
              <text style="font-size: 38rpx; font-weight: 600">{{ name }}</text>
              <button size="mini" style="margin-left: 30rpx" @click="copyToClipboard(name)">复制</button>
            </view>
          </view>
        </view>

        <!-- 信息 -->
        <view style="width: 95%; border: 0.5px solid gray; height: 0px; margin: 40rpx auto"></view>

        <view class="row-left" style="margin: 10rpx 20rpx">
          <text>初中毕业学校：</text>
          <text>{{ school }}</text>
        </view>

        <view class="row-left" style="margin: 10rpx 20rpx">
          <text>申请QQ号：</text>
          <view class="row-left">
            <text style="font-size: 30rpx; font-weight: 600; color: #3d71ff">{{ qq }}</text>
            <button size="mini" style="margin-left: 30rpx" @click="copyToClipboard(qq)">复制</button>
          </view>
        </view>

        <view class="row-left" style="margin: 10rpx 20rpx">
          <text v-if="passed === -1 || passed === 0">申请时间：</text>
          <text v-if="passed === 1">审核时间：</text>
          <text>{{ updated_at }}</text>
        </view>

        <view class="row-left" style="margin: 10rpx 20rpx">
          <text>审核状态：</text>
          <text v-if="passed === 0" style="color: #dd001b">未通过</text>
          <text v-if="passed === 1" style="color: #00c777">已通过</text>
        </view>
      </view>

      <view class="custom-title">录取通知书</view>

      <text v-if="imageLoading">请稍后……</text>
      <image :src="imageUrl" @tap="_previewImage(imageUrl)" mode="widthFix"></image>

      <button class="pass-button" @click="handlePass">通过</button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      school: '',
      qq: '',
      id: '',
      username: '',
      imageUrl: '',
      updated_at: '',
      passed: -1,
      imageLoading: true,
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
      }
    };
  },
  methods: {
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
    _previewImage(image) {
      var imgArr = [];
      imgArr.push(image);
      //预览图片
      uni.previewImage({
        urls: imgArr,
        current: imgArr[0]
      });
    },
    handleGetUserImage() {
      uni.request({
        url: `https://apis.johnsonsii.cn/apis/getuserimage/?username=${this.username}`,
        method: 'GET',
        responseType: 'arraybuffer',
        success: (res) => {
          const base64 = uni.arrayBufferToBase64(res.data);
          this.imageUrl = 'data:image/jpeg;base64,' + base64; // 将图片数据转换为 Base64 格式
          this.imageLoading = false;
        }
      });
    },
    handleGetUserInfo() {
      uni.request({
        url: `https://apis.johnsonsii.cn/apis/getuserinfo/?username=${this.username}`,
        method: 'GET',
        success: (res) => {
          this.id = res.data.id;
          this.username = res.data.username;
          this.name = res.data.name;
          this.school = res.data.school;
          this.qq = res.data.qq;
          this.updated_at = this.formatDate(res.data.updated_at);
          this.passed = res.data.passed;
        }
      });
    },
    formatDate(originalTime) {
      // 使用Date对象解析时间字符串
      var parsedTime = new Date(originalTime);

      // 获取年、月、日、小时、分钟和秒
      var year = parsedTime.getFullYear();
      var month = ('0' + (parsedTime.getMonth() + 1)).slice(-2);
      var day = ('0' + parsedTime.getDate()).slice(-2);
      var hours = ('0' + parsedTime.getHours()).slice(-2);
      var minutes = ('0' + parsedTime.getMinutes()).slice(-2);
      var seconds = ('0' + parsedTime.getSeconds()).slice(-2);

      // 格式化后的时间字符串
      var formattedTime = year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds;
      return formattedTime;
    },
    copyToClipboard(text) {
      uni.setClipboardData({
        data: text,
        success: function () {
          uni.showToast({
            title: '复制成功',
            icon: 'success'
          });
        },
        fail: function () {
          uni.showToast({
            title: '复制失败',
            icon: 'success'
          });
        }
      });
    },
    handlePass() {
      if (this.passed === 1) {
        uni.showToast({
          title: '已通过',
          icon: 'success'
        });
      } else {
        if (this.passed === -1) {
          uni.showToast({
            title: '请稍后……',
            icon: 'none'
          });
          return;
        }
        this.$refs.alertDialog.open();
      }
    },
    dialogConfirm() {
      this.loading = true;
      const self = this;
      uni.request({
        url: `https://apis.johnsonsii.cn/apis/setuserpassed?username=${this.username}&passed=1`,
        method: 'GET',
        success(res) {
          (self.loading = false),
            uni.showToast({
              title: '已通过',
              icon: 'success'
            });
          self.handleGetUserInfo();
        }
      });
    }
  },
  onLoad(option) {
    this.username = option.username;
    this.handleGetUserInfo();
    this.handleGetUserImage();
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
  width: 100%;
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
.infocard {
  width: 85%;
  height: calc(0.65 * 100vw);
  border-radius: 30rpx;
  box-shadow: 3rpx 3rpx 6rpx 2rpx rgba(0, 0, 0, 0.25);
  padding: 20rpx;
}

.custom-title {
  font-size: 50rpx;
  font-weight: 600;
  margin: 30rpx 0;
}

.col-left {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}

.col-left-between {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
}

.col-left-around {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: flex-start;
}

.col-left-top {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
}

.col-center-top {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}

.col-right-top {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-end;
}

.row-left {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}

.row-center {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.row-right {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
}

.flex {
  display: flex;
}

.col {
  flex-direction: col;
}

.row {
  flex-direction: row;
}

.center {
  justify-content: center;
  align-items: center;
}

text {
  font-size: 28rpx;
  color: rgb(10, 10, 10);
}

.pass-button {
  width: 90%;
  background-color: #3d71ff;
  border-radius: 50rpx;
  color: white;
  border: none;
  margin: 50rpx 0 200rpx 0;
}
</style>
