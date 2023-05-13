import os
import re
import itertools
import json
import pandas

def main(in_dir, relation, bars):
    files = list(
        filter(
            lambda x: bool(re.match(r".*\.csv", x)),
            os.listdir(in_dir)
        )
    )

    # Bars chart
    all_bar_chart_statistics = dict()
    # Arc Diagram
    all_arc_diagram_statistics = {
        "nodes": [],
        "links": []
    }

    for file in files:
        df = pandas.read_csv("{}/{}".format(in_dir, file))
        department = list(
            itertools.chain.from_iterable(
                ["、".join(i[1:]).split("、") for i in df[["專長", "特別門診"]].itertuples()] # 把專長和特別門診併一起
            )
        )

        # Todo for single case.
        # Bars chart
        single_bar_chart_statistics = dict()

        for i in department:
            if not i in single_bar_chart_statistics:
                single_bar_chart_statistics[i] = 1
            else:
                single_bar_chart_statistics[i] += 1

            if not i in all_bar_chart_statistics:
                all_bar_chart_statistics[i] = 1
            else:
                all_bar_chart_statistics[i] += 1

        with open("{}/{}csv".format(bars, file[:-3]), "+wt", encoding="utf-8-sig") as f:
            # Bar Chart
            print(
                "門診,次數",
                file=f
            )
            for k in single_bar_chart_statistics.keys():
                print(
                    "{},{}".format(k, single_bar_chart_statistics[k]),
                    file=f
                )

        # Arc Diagram
        single_arc_diagram_statistics = {
            "nodes": [],
            "links": []
        }
        # 醫生 Group 1, 醫院 Group 2, 門診 Group 3
        for i in df["姓名"].to_list():
            j = {"id": i, "group": 1}
            if not j in all_arc_diagram_statistics["nodes"]:
                all_arc_diagram_statistics["nodes"].append(j)
            if not j in single_arc_diagram_statistics["nodes"]:
                single_arc_diagram_statistics["nodes"].append(j)

        all_arc_diagram_statistics["nodes"].append({"id": file[:-4], "group": 3})

        for i in set(department):
            j = {"id": i, "group": 2}
            if not j in all_arc_diagram_statistics["nodes"]:
                all_arc_diagram_statistics["nodes"].append(j)
            if not j in single_arc_diagram_statistics["nodes"]:
                single_arc_diagram_statistics["nodes"].append(j)

        all_arc_diagram_statistics["links"] += [{"source": i, "target": file[:-4], "value": 1} for i in df["姓名"].to_list()] # 醫師-分院 1
        for _, name, expert, special in df[["姓名", "專長", "特別門診"]].itertuples(): # 醫師-門診 2
            for i in "{}、{}".format(expert, special).split("、"):
                all_arc_diagram_statistics["links"].append({"source": name, "target": i, "value": 2})
                single_arc_diagram_statistics["links"].append({"source": name, "target": i, "value": 2})
                j = {"source": file[:-4], "target": i}
                if not j in all_arc_diagram_statistics["links"]: all_arc_diagram_statistics["links"].append(j)

        with open("{}/{}.json".format(relation, file[:-4]), "+wt", encoding="utf-8-sig") as f:
            print(
                json.dumps(
                    single_arc_diagram_statistics,
                    sort_keys=True,
                    indent=4,
                    ensure_ascii=False
                ),
                file=f
            )


    # Todo for all case.
    # Bars chart
    with open("{}/all_bar_chart_statistics.csv".format(bars), "+wt", encoding="utf-8-sig") as f:
        print(
            "門診,次數",
            file=f
        )
        for k in all_bar_chart_statistics.keys():
                
                print(
                    "{},{}".format(k, all_bar_chart_statistics[k]),
                    file=f
                )


    # Arc Diagram
    with open("{}/all_arc_diagram_statistics.json".format(relation), "+wt", encoding="utf-8-sig") as f:
        print(
            json.dumps(
                all_arc_diagram_statistics,
                sort_keys=True,
                indent=4,
                ensure_ascii=False
            ),
            file=f
        )

main(
    "data/crawler_get_from_website",
    "data/relationship_network",
    "data/bars_chart"
)