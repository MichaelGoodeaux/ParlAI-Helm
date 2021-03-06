#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Prints validation statistics about API calls from a directory generated by
`tod_distributed_uber_script`.

This file assumes that there exists a "eval_stats.json" that includes validation
statistics from a valid run on OutDomainSystemTeacher of Google SGD's simulation
scripts; also assumes a file of the format `mm_eval*pro*st*` generated from validation
goals of the same source conversations, split by single goals.
"""

from parlai.core.params import ParlaiParser
from parlai.core.script import ParlaiScript
import glob
import json

API_CALL_NAMES = [
    "ShareLocation",
    "RequestPayment",
    "MakePayment",
    "FindApartment",
    "ScheduleVisit",
    "FindHomeByArea",
    "GetCarsAvailable",
    "ReserveCar",
]


class GetQuickEvalStatsDirScript(ParlaiScript):
    @classmethod
    def setup_args(cls):
        parser = ParlaiParser(False, False)
        parser.add_argument("-p", "--path", required=False, type=str)
        return parser

    def get_apis_from_eval_stats(self):
        report = self.eval_data["report"]
        result = {}
        for key in report:
            for call in API_CALL_NAMES:
                if call in key:
                    if call not in result:
                        result[call] = {}
                    result[call][key] = report[key]
        return result

    def get_apis_from_processed_stats(self):
        cand_files = glob.glob(f"{self.path}/mm_eval*pro*st*")  # eval stats
        if len(cand_files) == 0:
            cand_files = glob.glob(
                f"{self.path}/*pro*st*"
            )  # legacy before nucleus added
        if len(cand_files) == 0:
            print("NO PROCESSED STATS FILE FOUND!")
            return {}

        with open(cand_files[0]) as f:
            lines = [line.strip() for line in f.readlines()]
            for i in range(len(lines)):
                if "DELTAS" in lines[i]:
                    want = lines[i + 1 :]
                    break

        result = {}
        for line in want:
            key, value = line.strip().split('", [')
            for call in API_CALL_NAMES:
                if call in key:
                    if call not in result:
                        result[call] = {}
                    result[call][key] = value
        return result

    def get_align_apis(self):
        api_eval = self.get_apis_from_eval_stats()
        api_processed_stats = self.get_apis_from_processed_stats()
        if len(api_eval) != len(api_processed_stats):
            print(
                "LENGTH OF FILES NOT THE SAME: api_eval",
                len(api_eval),
                "api_processed_stats",
                len(api_processed_stats),
            ),
        merged = []
        for key in sorted(API_CALL_NAMES):
            if (
                key == "FindHomeByArea" and len(api_eval) > 0
            ):  # this one has an extra api call type in train with 6 samples
                if len(api_eval[key]) != len(api_processed_stats[key]):
                    api_eval[key][
                        "api-FindHomeByArea--area-has_garage-in_unit_laundry-intent-number_of_baths-number_of_beds"
                    ] = "NA"
            api_eval_calls = sorted(api_eval.get(key, {}).keys())
            api_processed_stats_here = sorted(api_processed_stats.get(key, {}).items())
            for i in range(max(len(api_eval_calls), len(api_processed_stats_here))):
                save_me = []
                if len(api_eval_calls) > i:
                    api_call = api_eval_calls[i]
                    save_me.append(api_call)
                    save_me.append(str(api_eval[key][api_call]))
                if len(api_processed_stats_here) > i:
                    save_me.append(api_processed_stats_here[i][1].replace("]", ""))
                merged.append(", ".join(save_me))
        for entry in merged:
            print(entry)

    def run(self):
        opt = self.opt
        path = opt["path"]
        self.path = path

        eval_stats = f"{path}/eval_stats.json"
        with open(eval_stats) as f:
            eval_data = json.load(f)
        self.eval_data = eval_data

        self.get_align_apis()


if __name__ == "__main__":
    GetQuickEvalStatsDirScript.main()
