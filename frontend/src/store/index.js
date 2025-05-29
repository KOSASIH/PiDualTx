import { createStore } from 'vuex';
import Web3 from 'web3';

export default createStore({
  state: {
    internalRate: 314159,
    externalRate: 0.8111,
    piPurityBadge: false,
    volatilityAlert: {
      changePercentage: 0,
      trend: 'Stable',
    },
    userAccount: null,
    userPiBalance: 0,
  },
  mutations: {
    SET_INTERNAL_RATE(state, rate) {
      state.internalRate = rate;
    },
    SET_EXTERNAL_RATE(state, rate) {
      state.externalRate = rate;
    },
    SET_PI_PURITY_BADGE(state, status) {
      state.piPurityBadge = status;
    },
    SET_VOLATILITY_ALERT(state, alert) {
      state.volatilityAlert = alert;
    },
    SET_USER_ACCOUNT(state, account) {
      state.userAccount = account;
    },
    SET_USER_PI_BALANCE(state, balance) {
      state.userPiBalance = balance;
    },
  },
  actions: {
    async fetchRatesAction({ commit }) {
      try {
        const response = await fetch('/api/rates');
        const data = await response.json();
        commit('SET_INTERNAL_RATE', parseFloat(data.internalRate));
        commit('SET_EXTERNAL_RATE', parseFloat(data.externalRate));
        commit('SET_VOLATILITY_ALERT', {
          changePercentage: 5, // You can compute this dynamically
          trend: 'Upward', // Placeholder
        });
      } catch (error) {
        console.error('Failed to fetch rates:', error);
      }
    },
    async fetchPredictedPrice({ commit, state }) {
      // Call your AI prediction backend service here
      // Example dummy predicted price based on external rate + a small premium
      const predictedPrice = state.externalRate * (1 + Math.random() * 0.1);
      commit('SET_EXTERNAL_RATE', predictedPrice);
    },
    async fetchAnalytics({ commit }) {
      // Fetch analytics data from backend and update state if needed
      // Placeholder: simulate volatility and trend update
      commit('SET_VOLATILITY_ALERT', {
        changePercentage: Math.random() * 10,
        trend: Math.random() > 0.5 ? 'Upward' : 'Downward',
      });
      return {
        volatility: Math.random() * 10,
        trend: Math.random() > 0.5 ? 'Upward' : 'Downward',
        labels: Array.from({ length: 30 }, (_, i) => `Day ${i + 1}`),
        prices: Array.from({ length: 30 }, () => 0.8 + Math.random() * 0.05),
      };
    },
    async refreshUserBalance({ commit, state }) {
      if (!state.userAccount) {
        commit('SET_USER_PI_BALANCE', 0);
        return;
      }
      try {
        if (window.ethereum) {
          const web3 = new Web3(window.ethereum);
          // Assuming the Pi token is ERC20 and contract address & ABI accessible
          const contractAddress = process.env.VUE_APP_CONTRACT_ADDRESS;
          const contractAbi = []; // Load ABI or import dynamically
          
          const contract = new web3.eth.Contract(contractAbi, contractAddress);
          // Note: Replace 'balanceOf' if PiDualTx differs
          const balanceWei = await contract.methods.balanceOf(state.userAccount).call();
          const balance = web3.utils.fromWei(balanceWei, 'ether');
          commit('SET_USER_PI_BALANCE', parseFloat(balance));
        } else {
          console.warn('Ethereum wallet not detected');
          commit('SET_USER_PI_BALANCE', 0);
        }
      } catch (error) {
        console.error('Failed to fetch user Pi balance:', error);
        commit('SET_USER_PI_BALANCE', 0);
      }
    },
    async connectWallet({ commit }) {
      if (window.ethereum) {
        try {
          const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
          commit('SET_USER_ACCOUNT', accounts[0]);
        } catch (error) {
          console.error('User rejected wallet connection:', error);
        }
      } else {
        console.warn('No Ethereum wallet found');
      }
    },
  },
  getters: {
    effectiveRate(state) {
      // Determine effective rate based on conditions; example only
      return state.internalRate;
    },
  },
});

