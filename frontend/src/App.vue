template>
  div id="app" class="app-container">
    AutonomousDualTx />
  /div>
/template>

script>
import AutonomousDualTx from './components/AutonomousDualTx.vue';

export default {
  name: 'App',
  components: {
    AutonomousDualTx,
  },
};
/script>

style scoped>
.app-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  min-height: 100vh;
  padding: 40px 20px;
  color: #ffffff;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}
</style>
