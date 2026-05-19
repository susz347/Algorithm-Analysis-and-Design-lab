#!/usr/bin/env python3
"""
Real-world datasets for 0/1 Knapsack Problem

This module provides real-world datasets for testing knapsack algorithms.
The datasets are based on actual scenarios and publicly available data.
"""

import csv
import io
from typing import List, Tuple
from knapsack_algorithms import KnapsackItem


class RealWorldDatasets:
    """
    Collection of real-world datasets for knapsack problem testing.
    """

    @staticmethod
    def create_synthetic_orlib_dataset() -> Tuple[List[KnapsackItem], int]:
        """
        Create a synthetic dataset similar to OR-Library format.

        This simulates the structure of OR-Library datasets which are commonly
        used in Operations Research for knapsack problems.
        Reference: http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files.html
        """
        # Create a dataset with 10 items and capacity 50
        items = [
            KnapsackItem(12, 4, "ORLib_Item_1"),
            KnapsackItem(15, 6, "ORLib_Item_2"),
            KnapsackItem(20, 8, "ORLib_Item_3"),
            KnapsackItem(25, 10, "ORLib_Item_4"),
            KnapsackItem(30, 12, "ORLib_Item_5"),
            KnapsackItem(35, 14, "ORLib_Item_6"),
            KnapsackItem(40, 16, "ORLib_Item_7"),
            KnapsackItem(45, 18, "ORLib_Item_8"),
            KnapsackItem(50, 20, "ORLib_Item_9"),
            KnapsackItem(55, 22, "ORLib_Item_10"),
        ]
        capacity = 100
        return items, capacity

    @staticmethod
    def create_investment_portfolio_dataset() -> Tuple[List[KnapsackItem], int]:
        """
        Create investment portfolio optimization dataset.

        This dataset simulates selecting investments with different costs and expected returns.
        Based on real stock market data patterns.
        """
        investments = [
            ("Tech Stock A", 50000, 8000),   # High risk, high return
            ("Tech Stock B", 30000, 5000),
            ("Blue Chip A", 40000, 6000),    # Medium risk, medium return
            ("Blue Chip B", 35000, 5500),
            ("Bond Fund A", 20000, 2500),    # Low risk, low return
            ("Bond Fund B", 15000, 2000),
            ("Real Estate A", 80000, 12000), # High investment, steady return
            ("Real Estate B", 60000, 9000),
            ("Commodity A", 25000, 4000),    # Volatile
            ("Commodity B", 30000, 4500),
            ("ETF A", 10000, 1500),         # Diversified, low cost
            ("ETF B", 12000, 1800),
            ("Startup A", 100000, 25000),   # Very high risk, very high return
            ("Startup B", 80000, 20000),
            ("Crypto A", 5000, 3000),       # Extremely volatile
            ("Crypto B", 8000, 4500),
        ]

        items = [KnapsackItem(weight, value, name) for name, weight, value in investments]
        budget = 300000  # $300k investment budget

        return items, budget

    @staticmethod
    def create_project_selection_dataset() -> Tuple[List[KnapsackItem], int]:
        """
        Create project selection dataset.

        Simulates selecting software development projects based on effort and business value.
        Inspired by real project management scenarios.
        """
        projects = [
            ("E-commerce Platform", 120, 95),    # High effort, high value
            ("Mobile App", 80, 70),
            ("Data Analytics Tool", 100, 85),
            ("CRM System", 90, 75),
            ("API Gateway", 60, 50),            # Medium effort, medium value
            ("Security Audit", 40, 60),
            ("Performance Optimization", 50, 55),
            ("Documentation Update", 20, 15),   # Low effort, low value
            ("Bug Fixes", 30, 25),
            ("UI Redesign", 70, 65),
            ("Database Migration", 110, 90),
            ("Testing Framework", 45, 40),
            ("DevOps Pipeline", 55, 60),
            ("Machine Learning Model", 140, 100), # Very high effort, very high value
            ("Cloud Migration", 130, 95),
            ("Legacy System Update", 95, 70),
        ]

        items = [KnapsackItem(effort, value, name) for name, effort, value in projects]
        max_effort = 400  # Maximum development effort available

        return items, max_effort

    @staticmethod
    def create_nutrition_optimization_dataset() -> Tuple[List[KnapsackItem], int]:
        """
        Create nutrition optimization dataset.

        Selects food items to maximize nutrition while staying within calorie limit.
        Based on USDA nutrition data patterns.
        """
        foods = [
            ("Salmon (100g)", 208, 250),      # High protein, omega-3
            ("Quinoa (100g)", 368, 120),      # Complete protein, fiber
            ("Spinach (100g)", 23, 180),      # Iron, vitamins (low calories)
            ("Avocado (100g)", 160, 140),     # Healthy fats
            ("Greek Yogurt (100g)", 59, 200),  # Protein, probiotics
            ("Almonds (100g)", 579, 160),     # Vitamin E, healthy fats
            ("Sweet Potato (100g)", 86, 110),  # Vitamin A, fiber
            ("Broccoli (100g)", 34, 150),      # Vitamin C, fiber
            ("Eggs (100g)", 155, 180),        # Complete protein
            ("Blueberries (100g)", 57, 130),   # Antioxidants
            ("Chicken Breast (100g)", 165, 220), # Lean protein
            ("Brown Rice (100g)", 111, 90),    # Complex carbs
            ("Walnuts (100g)", 654, 140),     # Omega-3 fatty acids
            ("Kale (100g)", 35, 170),         # Vitamins K, A, C
            ("Tuna (100g)", 144, 200),        # Lean protein, omega-3
            ("Oats (100g)", 389, 100),        # Fiber, slow-release carbs
        ]

        items = [KnapsackItem(calories, nutrition_score, name) for name, calories, nutrition_score in foods]
        calorie_limit = 2000  # Daily calorie limit

        return items, calorie_limit

    @staticmethod
    def create_logistics_dataset() -> Tuple[List[KnapsackItem], int]:
        """
        Create logistics/shipping optimization dataset.

        Selects packages to ship while maximizing value within weight constraints.
        Based on real logistics scenarios.
        """
        packages = [
            ("Electronics Package A", 15, 5000),   # High value, medium weight
            ("Electronics Package B", 20, 6000),
            ("Clothing Package A", 8, 800),       # Low value, low weight
            ("Clothing Package B", 12, 1200),
            ("Books Package A", 25, 600),         # Low value, high weight
            ("Books Package B", 30, 750),
            ("Jewelry Package", 2, 15000),        # Very high value, very low weight
            ("Artwork Package", 35, 8000),        # High value, high weight
            ("Medical Supplies", 18, 3000),       # Medium value, medium weight
            ("Food Package A", 22, 1500),         # Perishable, medium value
            ("Food Package B", 16, 1800),
            ("Documents", 5, 2000),               # High value, very low weight
            ("Machinery Parts", 45, 4000),        # Heavy, medium value
            ("Cosmetics", 6, 2500),               # Medium value, low weight
            ("Sports Equipment", 28, 2200),       # Medium value, medium-high weight
            ("Toys Package", 14, 900),            # Low-medium value, medium weight
        ]

        items = [KnapsackItem(weight, value, name) for name, weight, value in packages]
        weight_limit = 100  # Weight limit in kg

        return items, weight_limit

    @staticmethod
    def get_all_real_world_datasets() -> dict:
        """
        Get all real-world datasets.
        """
        datasets = {}

        # Investment Portfolio Dataset
        items, capacity = RealWorldDatasets.create_investment_portfolio_dataset()
        datasets['Investment Portfolio'] = {
            'items': items,
            'capacity': capacity,
            'description': 'Investment selection with budget constraint',
            'source': 'Synthetic data based on real market patterns'
        }

        # Project Selection Dataset
        items, capacity = RealWorldDatasets.create_project_selection_dataset()
        datasets['Project Selection'] = {
            'items': items,
            'capacity': capacity,
            'description': 'Software project selection with effort constraint',
            'source': 'Synthetic data based on real project management scenarios'
        }

        # Nutrition Optimization Dataset
        items, capacity = RealWorldDatasets.create_nutrition_optimization_dataset()
        datasets['Nutrition Optimization'] = {
            'items': items,
            'capacity': capacity,
            'description': 'Food selection for nutrition within calorie limit',
            'source': 'Based on USDA nutrition data patterns'
        }

        # Logistics Dataset
        items, capacity = RealWorldDatasets.create_logistics_dataset()
        datasets['Logistics'] = {
            'items': items,
            'capacity': capacity,
            'description': 'Package selection for shipping optimization',
            'source': 'Synthetic data based on real logistics scenarios'
        }

        # Synthetic OR-Library Dataset
        items, capacity = RealWorldDatasets.create_synthetic_orlib_dataset()
        datasets['OR-Library Style'] = {
            'items': items,
            'capacity': capacity,
            'description': 'Synthetic dataset in OR-Library format',
            'source': 'Synthetic data based on OR-Library patterns (http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files.html)'
        }

        return datasets


def demonstrate_real_world_usage():
    """
    Demonstrate the usage of real-world datasets.
    """
    from knapsack_algorithms import KnapsackBenchmark

    datasets = RealWorldDatasets.get_all_real_world_datasets()
    benchmark = KnapsackBenchmark()

    print("真实世界背包问题数据集")
    print("=" * 50)

    for dataset_name, data in datasets.items():
        print(f"\n{dataset_name}:")
        print(f"  描述: {data['description']}")
        print(f"  来源: {data['source']}")
        print(f"  物品数量: {len(data['items'])}")
        print(f"  容量/约束: {data['capacity']}")
        print(f"  约束类型: {'预算' if 'Investment' in dataset_name else '工作量' if 'Project' in dataset_name else '卡路里' if 'Nutrition' in dataset_name else '重量(公斤)'}")

        # 为此数据集运行基准测试
        results = benchmark.run_benchmark(data['items'], data['capacity'])
        benchmark.print_results(results, dataset_name)

        # 显示最佳算法选择的物品
        best_algorithm = max(
            [(name, result) for name, result in results.items() if 'total_value' in result],
            key=lambda x: x[1]['total_value']
        )

        print(f"\n最佳解决方案 ({best_algorithm[0]}):")
        for item in best_algorithm[1]['selected_items'][:5]:  # 显示前5个物品
            print(f"  - {item.name}: 重量={item.weight}, 价值={item.value}")
        if len(best_algorithm[1]['selected_items']) > 5:
            print(f"  ... 还有 {len(best_algorithm[1]['selected_items']) - 5} 个物品")


if __name__ == "__main__":
    demonstrate_real_world_usage()