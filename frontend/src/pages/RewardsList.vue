<template>
    <div class="row">
      <div class="col-12">
        <card :title="rewards.title" :subTitle="rewards.subTitle">
          <div slot="raw-content" class="table-responsive">
            <paper-table type="hover" :title="rewards.title" :sub-title="rewards.subTitle" :data="rewards.data"
                         :columns="rewards.columns">

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
      rewards: {
        title: "Reward History",
        subTitle: "List of past rewards",
        columns: ["token", "value", "timestamp"],
        data: [{
          token:	"",
          value:	0,
          timestamp:	""
        }]
      }
    };
  },
  mounted() {
    axios.get("/api/rewards")
    .then(response => {
      this.rewards.data = response.data
    })
  },
};
</script>
<style>
</style>
