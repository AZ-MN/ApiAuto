"""
pip install pytest allure-pyetst -i https://pypi.tuna.tsinghua.edu.cn/simple/
"""
import xml.etree.cElementTree as ET
import json, os, uuid
import sys
from pathlib import Path


def checkChildren(
        xmlObject, checkString, num, result, demoFile, featureIndex, storyIndex
):
    for children in xmlObject:
        try:
            if num == 1 and children.attrib["sby"] != "0":
                featureIndexStr = (
                    "#" + str(featureIndex) + " "
                    if featureIndex >= 10
                    else "#0" + str(featureIndex) + " "
                )
                result["feature"] = featureIndexStr + children.attrib["lb"]
                featureIndex += 1
            if num >= 2 and children.tag == "sample":
                storyIndexStr = (
                    "#" + str(storyIndex) + " "
                    if storyIndex >= 10
                    else "#0" + str(storyIndex) + " "
                )
                result["story"] = storyIndexStr + children.attrib["lb"]
                storyIndex += 1
        except:
            pass
        if children.tag == checkString:
            result["case_name"] = children.attrib["lb"]
            for httpSampleChildren in children:
                result[httpSampleChildren.tag] = httpSampleChildren.text
                if httpSampleChildren.tag == "assertionResult":
                    for assertionResultChildren in httpSampleChildren:
                        result[
                            assertionResultChildren.tag
                        ] = assertionResultChildren.text
            feature = result["feature"] if "feature" in result else None
            story = result["story"] if "story" in result else None
            case_name = result["case_name"] if "case_name" in result else None
            URL = result["java.net.URL"] if "java.net.URL" in result else None
            method = result["method"] if "method" in result else None
            requestHeader = (
                result["requestHeader"] if "requestHeader" in result else None
            )
            queryString = result["queryString"] if "queryString" in result else None
            responseData = result["responseData"] if "responseData" in result else None
            failureMessage = (
                result["failureMessage"] if "failureMessage" in result else None
            )
            print(f'{result=}')
            failure = result["failure"] if "failure" in result else "false"
            # print(feature, story, case_name, failureMessage, URL)
            storyString = (
                "@allure.story('" + result["story"] + "') # 二级目录"
                if "story" in result
                else ""
            )
            pyString = """
@allure.feature('{feature}') # 一级目录{story}
@allure.title("{case_name}")
def test_allure_report_{num}():
    with allure.step('请求url：{URL}'):
        print('请求url：{URL}')
    with allure.step('请求方法：{method}' ):
        print('请求方法：{method}' )
    with allure.step('请求头：{requestHeader}' ):
        print('请求头：{requestHeader}' )
    with allure.step('''请求数据：{queryString}'''):
        print('''请求数据：{queryString}''')
    with allure.step('''接口返回：{responseData}'''):
        print('''接口返回：{responseData}''')
    with allure.step('''断言结果：{failureMessage}'''):
        print('''断言结果：{failureMessage}''')
    assert "{failure}" == 'false' """.format(
                feature=feature,
                story=storyString,
                case_name=case_name,
                num=str(uuid.uuid1()).replace("-", ""),
                URL=URL,
                method=method,
                requestHeader=str(requestHeader).replace("\n", "").replace("\r", ""),
                queryString=str(json.dumps(queryString)).replace("'", '"'),
                responseData=str(json.dumps(responseData)).replace("'", '"'),
                failureMessage=str(failureMessage).replace("'", '"'),
                failure=failure,
            )
            # print(pyString)
            with open(demoFile, "a", encoding="utf-8") as c:
                c.write(pyString)
        else:
            checkChildren(
                children,
                checkString,
                num + 1,
                result,
                demoFile,
                featureIndex,
                storyIndex,
            )


if __name__ == "__main__":
    # 通过命令行来执行 ，例如python3 JtlToReportHTML.py test.jtl test_demo.py report
    _self_path, jtl_path, report_path, allure_path, *_ = sys.argv

    jtl_path = Path(jtl_path)
    report_path = Path(report_path)
    report_resource = report_path / "resource"
    report_html = report_path / "html"
    tmp_file_path = Path("test.py")

    with open(tmp_file_path, "w", encoding="utf-8") as demo:
        demo.write(
            """
# -*- coding: utf-8 -*-
import allure
"""
        )

    tree = ET.parse(str(jtl_path))
    root = tree.getroot()

    checkChildren(root, "httpSample", 1, {}, str(tmp_file_path), 1, 1)

    pyString = f"{sys.executable} -m pytest --capture=sys {tmp_file_path}  --alluredir {report_resource} --clean-alluredir -qq"
    os.system(pyString)

    alSring = (
        f"{allure_path} generate   {report_resource}  -o {report_html} --single-file --clean"
    )
    os.system(alSring)
    #
    tmp_file_path.unlink(True)
    # report_resource.unlink(True)

    os.system(f'{report_html / "index.html"}')
