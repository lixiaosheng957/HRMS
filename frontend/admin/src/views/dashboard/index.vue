<template>
  <div class="dashboard-container">
    <div>
      代办事项
    </div>
    <div>
      人事变动
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard'
  // computed: {
  //   ...mapGetters([
  //     'name'
  //   ])
  // }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
