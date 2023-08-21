<template>
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
      <view class="custom-title f1 center">管理员后台</view>
      <view class="center" style="width: 100rpx" @click="handleMagic">
        <uni-icons type="smallcircle" color="white" size="26"></uni-icons>
      </view>
    </view>

    <!-- 文档流占位元素 -->
    <view class="fake-header"></view>

    <!-- 正文 -->
    <view class="content coll">
      <view class="selector">
        <checkbox style="transform: scale(0.8)" color="#3D71FF" :checked="checkBoxChecked" @click="handleSelector" />
        <text @click="handleSelector">仅显示未通过审核的人员</text>
      </view>
      <uni-table ref="table" :loading="loading" border stripe type="selection" emptyText="暂无更多数据" @selection-change="selectionChange">
        <uni-tr>
          <uni-th width="130" align="center">日期</uni-th>
          <uni-th width="100" align="center">姓名</uni-th>
          <uni-th width="100" align="center">是否审核</uni-th>
          <uni-th width="150" align="center">详细信息</uni-th>
        </uni-tr>
        <uni-tr v-for="(item, index) in tableData" :key="index">
          <uni-td align="center">{{ item.updated_at }}</uni-td>
          <uni-td align="center">{{ item.name }}</uni-td>
          <uni-td align="center">{{ item.passed }}</uni-td>
          <uni-td align="center">
            <button class="pass-button" @click="handlePassManagement(item)">审核管理</button>
          </uni-td>
        </uni-tr>
      </uni-table>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      tableData: [],
      checkBoxChecked: false,
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
    handlePassManagement(item) {
      uni.navigateTo({
        url: `/pages/info/info?username=${item.username}`
      });
    },
    handleSelector() {
      if (this.checkBoxChecked === false) {
        this.checkBoxChecked = true;
        this.handleUpdate('https://apis.johnsonsii.cn/apis/getallnotpass/');
      } else {
        this.checkBoxChecked = false;
        this.handleUpdate('https://apis.johnsonsii.cn/apis/getall/');
      }
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
    handleUpdate(customUrl) {
      const self = this;
      uni.request({
        url: customUrl,
        success(res) {
          // 请求成功后处理返回的数据
          if (res.statusCode === 200) {
            const responseData = res.data;
            self.tableData = [];
            responseData.forEach((item) => {
              self.tableData.push({
                id: item.id,
                username: item.username,
                updated_at: self.formatDate(item.updated_at),
                name: item.name,
                passed: item.passed === 0 ? '未审核' : '已通过'
              });
            });
          }
        },
        fail(error) {
          console.log(error);
        }
      });
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
    }
  },
  onLoad(option) {
    this.username = option.username;
    if (this.username === '') {
      uni.navigateTo({
        url: '/pages/login/login'
      });
    }
    uni.request({
      url: `https://apis.johnsonsii.cn/apis/getuserinfo?username=${username}`,
      success: (res) => {
        if (res.data === 0 || res.data.role === 0) {
          uni.navigateTo({
            url: '/pages/login/login'
          });
        }
      }
    });

    if (this.checkBoxChecked === true) {
      this.handleUpdate('https://apis.johnsonsii.cn/apis/getallnotpass/');
    } else {
      this.handleUpdate('https://apis.johnsonsii.cn/apis/getall/');
    }
  },
  onShow() {
    if (this.checkBoxChecked === true) {
      this.handleUpdate('https://apis.johnsonsii.cn/apis/getallnotpass/');
    } else {
      this.handleUpdate('https://apis.johnsonsii.cn/apis/getall/');
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
.selector {
  display: flex;
  flex-direction: row;
  margin: 30rpx 0;
  align-items: center;
  padding-left: 30rpx;
}
.selector text {
  font-size: 27rpx;
  margin-left: 14rpx;
  color: gray;
}
.pass-button {
  height: 100%;
  width: 100%;
  background-color: rgb(253, 253, 253);
  font-size: 28rpx;
  color: #3d71ff;
}
.pass-button:active {
  background-color: rgb(220, 220, 220);
}
</style>
