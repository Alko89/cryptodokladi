<template>
  <div>
    <!--Stats cards-->
    <div class="row">
      <div class="col-md-6 col-xl-3" v-for="stats in statsCards" :key="stats.title">
        <stats-card>
          <div class="icon-big text-center" :class="`icon-${stats.type}`" slot="header">
            <i :class="stats.icon"></i>
          </div>
          <div class="numbers" slot="content">
            <p>{{stats.title}}</p>
            {{stats.value}}
          </div>
          <div class="stats" slot="footer">
            <i :class="stats.footerIcon"></i> {{stats.footerText}}
          </div>
        </stats-card>
      </div>
    </div>

    <!--Charts-->
    <div class="row">
      <div class="col-md-6 col-12">
        <card>
          <template slot="header">
            <h4 class="card-title">
              <slot name="title">PIVX</slot>
            </h4>
            <p class="card-category">
              <slot name="subTitle">All Time</slot>
            </p>
          </template>
          <apexcharts type="area" height="245" :options="transactionsChart.options" :series="transactionsChart.series"/>
        </card>
      </div>

      <div class="col-md-6 col-12">
        <card>
          <template slot="header">
            <h4 class="card-title">
              <slot name="title">Rewards distribution</slot>
            </h4>
            <p class="card-category">
              <slot name="subTitle">All Time</slot>
            </p>
          </template>
          <apexcharts type="pie" height="245" :options="rewardsDistribution.options" :series="rewardsDistribution.series"/>
        </card>
      </div>
    </div>
  </div>
</template>
<script>
import { StatsCard } from "@/components/index";
import VueApexCharts from "vue-apexcharts";

import axios from "axios";

export default {
  mounted() {
    axios.get("/api/tokens").then(response => {
      this.tokens = response.data;

      this.tokens.forEach(token => {
        switch (token.token) {
          case "PIVX":
            axios.get("/api/transactions/" + this.user.name + "/PIVX").then(response => {
              this.transactions.token = "PIVX";
              this.transactions.transactions = response.data;

              var series = [];
              var labels = [];
              var value = 0;
              response.data.forEach(transaction => {
                if (transaction.sender == this.user.name)
                  value -= transaction.value;
                else
                  value += transaction.value;
                labels.push(transaction.timestamp);
                series.push(value);
              });

              this.transactionsChart.options = {
                colors: ['purple'],
                dataLabels: {
                  enabled: false
                },
                stroke: {
                  curve: "smooth"
                },

                xaxis: {
                  type: "datetime",
                  categories: labels
                },
                tooltip: {
                  x: {
                    format: "dd/MM/yy HH:mm"
                  }
                }
              }
              this.transactionsChart.series = [
                {
                  name: "PIVX",
                  data: series
                }
              ];

              axios.get("/api/ticker/PIVX").then(response => {
                var card = {
                  type: "purple",
                  icon: "cf cf-pivx",
                  title: token.name,
                  value: value.toFixed(2) + token.token,
                  footerText: (value * response.data[0].price_eur).toFixed(2),
                  footerIcon: "fas fa-euro-sign"
                }

                this.statsCards.push(card);

                axios.get("/api/token/PIVX").then(response => {
                  var total = response.data.total;
                  var ratio = 100 * value / total;
                  this.rewardsDistribution.series = [ ratio, 100 - ratio ];
                });
              });
            });
            break;
          default:
            axios.get("/api/transactions/" + this.user.name + "/" + token.token).then(response => {
              if (response.data.length != 0) {
              var value = 0;
              response.data.forEach(transaction => {
                if (transaction.sender == this.user.name)
                  value -= transaction.value;
                else
                  value += transaction.value;
              });

              var card = {
                type: "info",
                icon: "cf cf-doge",
                title: token.name,
                value: value.toFixed(2) + token.token,
                footerText: (value * response.data[0].price_eur).toFixed(2),
                footerIcon: "fas fa-euro-sign"
              }

              switch (token.token) {
                  case "BTC":
                    card.type = "warning";
                    card.icon = "cf cf-btc";
                    break;
                  case "ETH":
                    card.type = "purple";
                    card.icon = "cf cf-eth";
                    break;
                  case "XMR":
                    card.type = "danger";
                    card.icon = "cf cf-xmr";
                    break;
                  default:
                }

                this.statsCards.push(card);

                axios.get("/api/ticker/" + token.name).then(response => {
                  card.footerText = (value * response.data[0].price_eur).toFixed(2)
                });
              }
            });
            break;
        }
      });
    });
  },
  components: {
    StatsCard,
    apexcharts: VueApexCharts
  },
  /**
   * Chart data used to render stats, charts. Should be replaced with server data
   */
  data() {
    return {
      user: this.$store.getters.getUserData,
      transactionsChart: {
        series: [],
        options: {}
      },
      rewardsDistribution: {
        series: [50, 50],
        options: {
          labels: ['Owned', 'Rest'],
          theme: {
            palette: 'palette10'
          },
          responsive: [{
            breakpoint: 480,
            options: {
              chart: {
                width: 200
              },
              legend: {
                position: 'bottom'
              }
            }
          }]
        }
      },

      tokens: [
        {
          name: "",
          token: ""
        }
      ],
      transactions: [
        {
          token: "",
          transactions: [
            {
              id: 0,
              user: 0,
              sender: null,
              value: 0,
              timestamp: "",
              comment: ""
            }
          ]
        }
      ],
      statsCards: []
    };
  }
};
</script>
<style>
</style>
