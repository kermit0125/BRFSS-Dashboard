# run_cleaning_pipeline.py
# 作用：整合所有数据清理步骤，按顺序依次执行
# 使用方法：python run_cleaning_pipeline.py

import os
import sys
import subprocess
import time
from pathlib import Path

# ===== 配置 =====
SCRIPT_DIR = Path(__file__).parent.absolute()
os.chdir(SCRIPT_DIR)

def print_header(text):
    """打印标题"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")

def print_step(num, total, name):
    """打印步骤信息"""
    print(f"\n[{num}/{total}] {name}")
    print("-" * 80)

def run_script(script_name, description):
    """运行Python脚本"""
    script_path = Path(script_name)
    
    if not script_path.exists():
        print(f"⚠️  跳过: 脚本不存在 {script_name}")
        return True
    
    print(f"📝 {description}")
    print(f"   执行: python {script_name}\n")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=SCRIPT_DIR,
            check=False,
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"\n✅ 完成 (耗时: {elapsed:.2f} 秒)")
            return True
        else:
            print(f"\n❌ 失败 (退出码: {result.returncode}, 耗时: {elapsed:.2f} 秒)")
            return False
            
    except Exception as e:
        print(f"\n❌ 异常: {str(e)}")
        return False

def check_output_file(filename):
    """检查输出文件是否存在并显示大小"""
    filepath = Path(filename)
    if filepath.exists():
        size = filepath.stat().st_size
        if size > 1024 * 1024:
            size_str = f"{size / (1024 * 1024):.2f} MB"
        elif size > 1024:
            size_str = f"{size / 1024:.2f} KB"
        else:
            size_str = f"{size} bytes"
        return True, size_str
    return False, None

def main():
    """主函数"""
    print_header("BRFSS 数据清理流程")
    print(f"工作目录: {os.getcwd()}")
    print(f"Python: {sys.version.split()[0]}\n")
    
    # 检查原始数据
    if not Path("dataset.csv").exists():
        print("❌ 错误: 'dataset.csv' 文件不存在！")
        print("请确保原始数据文件在当前目录中。")
        return False
    
    total_start = time.time()
    
    # 定义清理步骤
    steps = [
        {
            "name": "Step0: 数据预处理",
            "script": "data_clean_Step0_preprocessing.py",
            "required": False,
            "output": "dataset_preprocessed.csv",
        },
        {
            "name": "Step1: QuestionID 合并",
            "script": "data_clean_Step1.py",
            "required": True,
            "output": "cleaned_data_question_merged.csv",
        },
        {
            "name": "Step2: ResponseID 和 Response 合并",
            "script": "data_clean_Step2.py",
            "required": True,
            "output": "cleaned_data_response_merged.csv",
        },
        {
            "name": "Step3: BreakoutID 和 Break_Out 合并",
            "script": "data_clean_Step3.py",
            "required": True,
            "output": "cleaned_data_breakout_merged.csv",
        },
        {
            "name": "Step4: 数值清洗",
            "script": "data_clean_Step4.py",
            "required": True,
            "output": "cleaned_data_final.csv",
        },
        {
            "name": "Step5: 数据聚合",
            "script": "data_clean_Step5.py",
            "required": True,
            "output": "cleaned_data_final.parquet",
        },
        {
            "name": "Step6: 数据质量增强和验证",
            "script": "data_clean_Step6.py",
            "required": False,
            "output": "cleaned_data_final_enhanced.parquet",
        },
    ]
    
    # 执行步骤
    success_count = 0
    failed_steps = []
    
    for i, step in enumerate(steps, 1):
        print_step(i, len(steps), step['name'])
        
        success = run_script(step['script'], step['name'])
        
        if success:
            # 检查输出文件
            exists, size_str = check_output_file(step['output'])
            if exists:
                print(f"📊 输出: {step['output']} ({size_str})")
            elif step['required']:
                print(f"⚠️  警告: 输出文件未生成 {step['output']}")
            
            success_count += 1
        else:
            failed_steps.append(step['name'])
            if step['required']:
                print(f"\n❌ 必需步骤失败，停止执行")
                response = input("\n是否继续执行后续步骤？(y/n): ").strip().lower()
                if response != 'y':
                    break
    
    # 总结
    total_elapsed = time.time() - total_start
    
    print_header("执行总结")
    print(f"✅ 成功: {success_count}/{len(steps)} 步骤")
    
    if failed_steps:
        print(f"❌ 失败: {len(failed_steps)} 步骤")
        for name in failed_steps:
            print(f"   - {name}")
    
    print(f"\n⏱️  总耗时: {total_elapsed:.2f} 秒 ({total_elapsed/60:.2f} 分钟)")
    
    # 检查最终文件
    print("\n📁 最终输出文件:")
    final_files = [
        ("cleaned_data_final.parquet", "标准版本"),
        ("cleaned_data_final_enhanced.parquet", "增强版本（推荐）"),
    ]
    
    for filename, desc in final_files:
        exists, size_str = check_output_file(filename)
        if exists:
            print(f"   ✅ {filename} ({desc}) - {size_str}")
        else:
            print(f"   ⚠️  {filename} ({desc}) - 不存在")
    
    # 检查质量报告
    if Path("data_quality_report.txt").exists():
        print("\n📊 数据质量报告: data_quality_report.txt")
        print("   建议查看报告以了解数据质量情况")
    
    if success_count == len(steps):
        print("\n🎉 所有步骤执行成功！")
        print("\n💡 下一步:")
        print("   1. 查看 data_quality_report.txt 了解数据质量")
        print("   2. 使用 cleaned_data_final_enhanced.parquet 更新 dashboard_app.py")
        return True
    else:
        print(f"\n⚠️  有 {len(failed_steps)} 个步骤失败，请检查错误信息")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断执行")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

