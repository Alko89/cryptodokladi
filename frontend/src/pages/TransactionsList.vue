<template>
    <div class="row">
      <div class="col-12">
        <card :title="transactions.title" :subTitle="transactions.subTitle">
          <div slot="raw-content" class="table-responsive">
            <paper-table type="hover" :title="transactions.title" :sub-title="transactions.subTitle" :data="transactions.data"
                         :columns="transactions.columns">

            </paper-table>
          </div>
        </card>
      </div>
    </div>
</template>
<script>
import { PaperTable } from "@/components";

import axios from 'axios'

export default {
  components: {
    PaperTable
  },
  data() {
    return {
      user: this.$store.getters.getUserData,
      transactions: {
        title: "Transactions",
        subTitle: "List of transactions",
        columns: ["token", "value", "timestamp", "comment"],
        data: [{
          token:	"",
          value:	0,
          timestamp:	"",
          comment:	"",
          user:	"",
          sender:	""
        }]
      }
    };
  },
  mounted() {
    axios.get("/api/user_transactions/" + this.user.name)
    .then(response => {
      this.transactions.data = response.data
    })
  },
};
</script>
<style>
</style>
