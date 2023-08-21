<template>
  <view class="container">
    <!-- 导航栏 -->
    <view class="header flexr fab sac whitefont smallshadow" :style="headerStyle">
      <view class="center" style="width: 100rpx" @click="handleBack">
        <uni-icons type="undo-filled" color="white" size="26"></uni-icons>
      </view>
      <view class="custom-title f1 center">测试</view>
      <view class="center" style="width: 100rpx" @click="handleMagic">
        <uni-icons type="smallcircle" color="white" size="26"></uni-icons>
      </view>
    </view>

    <!-- 文档流占位元素 -->
    <view class="fake-header"></view>

    <!-- 正文 -->
    <view class="content dev">
      Lorem ipsum dolor sit, amet consectetur adipisicing elit. Provident tempora cum ut pariatur eveniet ipsa quidem officia voluptatibus? Incidunt illo neque itaque non nobis
      laudantium placeat pariatur tempore magni eius!
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
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

.content {
  height: 200vh;
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
</style>
