<template>
  <div class="autonomous-dual-tx">
    <u-navbar :title="$t('transaction.title')" />
    <u-tabs :list="tabs" v-model="activeTab">
      <u-tab-pane :label="$t('transaction.tabTransaction')" name="transaction">
        <u-card>
          <p>{{ $t('transaction.predictedPrice') }}: ${{ predictedPrice.toFixed(4) }} USD/Pi</p>
          <u-input v-model="transactionAmount" placeholder="Enter amount in Pi" type="number" />
          <u-button @click="executeTransaction" :disabled="!isTransactionValid">{{ $t('transaction.execute') }}</u-button>
          <u-alert v-if="transactionStatus" :type="transactionStatus.type">{{ transactionStatus.message }}</u-alert>
        </u-card>
      </u-tab-pane>
      <u-tab-pane :label="$t('transaction.tabAnalytics')" name="analytics">
        <u-chart type="line" :data="chartData" />
        <u-card>
          <h3>{{ $t('transaction.analyticsTitle') }}</h3>
          <p>{{ $t('transaction.volatility') }}: {{ volatility }}%</p>
          <p>{{ $t('transaction.marketTrend') }}: {{ marketTrend }}</p>
        </u-card>
      </u-tab-pane>
    </u-tabs>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import Web3 from 'web3';
import PiDualTxABI from '@/abis/PiDualTx.json';

export default {
  data() {
    return {
      activeTab: 'transaction',
      tabs: [
        { name: 'transaction', label: this.$t('transaction.tabTransaction') },
        { name: 'analytics', label: this.$t('transaction.tabAnalytics') },
      ],
      predictedPrice: 0.8111,
      transactionAmount: 0,
      transactionStatus: null,
      chartData: { labels: [], datasets: [] },
      volatility: 0,
      marketTrend: '',
    };
  },
  computed: {
    ...mapState(['internalRate', 'externalRate', 'piPurityBadge', 'volatilityAlert']),
    effectiveRateType() {
      return this.form.transactionMode === 'auto' &&
        (this.piPurityBadge || this.volatilityAlert.changePercentage > 5 ||
         Math.abs((this.predictedPrice - this.externalRate) / this.externalRate) * 100 > 5)
        ? 'internal' : 'external';
    },
    isTransactionValid() {
      return this.transactionAmount > 0;
    },
  },
  methods: {
    ...mapActions(['fetchRatesAction', 'fetchPredictedPrice', 'fetchAnalytics']),
    
    async executeTransaction() {
      try {
        const web3 = new Web3(window.ethereum);
        const contract = new web3.eth.Contract(PiDualTxABI, process.env.VUE_APP_CONTRACT_ADDRESS);
        const accounts = await web3.eth.getAccounts();
        
        const tx = await contract.methods.executeTransaction(this.transactionAmount).send({ from: accounts[0] });
        this.transactionStatus = { type: 'success', message: this.$t('transaction.successMessage', { txHash: tx.transactionHash }) };
      } catch (error) {
        this.transactionStatus = { type: 'error', message: this.$t('transaction.errorMessage') };
      }
    },

    async fetchAnalyticsData() {
      const analyticsData = await this.fetchAnalytics();
      this.volatility = analyticsData.volatility;
      this.marketTrend = analyticsData.trend;
      this.chartData = {
        labels: analyticsData.labels,
        datasets: [
          {
            label: this.$t('transaction.priceHistory'),
            data: analyticsData.prices,
            borderColor: '#42A5F5',
            fill: false,
          },
        ],
      };
    },
  },
  mounted() {
    this.fetchRatesAction();
    this.fetchPredictedPrice();
    this.fetchAnalyticsData();
  },
};
</script>

<style scoped>
.autonomous-dual-tx {
  padding: 20px;
}
</style>
