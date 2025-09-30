import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_daily_milk_received(month_data, col_name):
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.lineplot(data=month_data, x='Date of Record', y=col_name, marker='o', ax=ax, label='Milk Received')
    plt.xticks(rotation=45)
    ax.legend(title='Legend')
    plt.tight_layout()
    return fig

def plot_milk_received_by_status(month_data, col_name):
    fig, ax = plt.subplots(figsize=(8, 4))
    status_sum = month_data.groupby('Milk Received?')[col_name].sum().reset_index()
    sns.barplot(x='Milk Received?', y=col_name, data=status_sum, palette='Set2', ax=ax)
    ax.legend(title='Milk Received Status')
    plt.tight_layout()
    return fig

def plot_milk_received_ratio(month_data):
    counts = month_data['Milk Received?'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['#4CAF50', '#F44336'], startangle=90)
    ax.axis('equal')
    ax.legend(wedges, counts.index, title='Milk Received?', loc='best')
    return fig

def plot_milk_quantity_distribution(month_data, col_name):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(month_data[col_name], bins=20, kde=True, ax=ax)
    ax.legend(['Milk Quantity'])
    plt.tight_layout()
    return fig

def plot_average_daily_milk(month_data, col_name):
    avg_daily = month_data.groupby('Date of Record')[col_name].mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.scatterplot(data=avg_daily, x='Date of Record', y=col_name, ax=ax)
    plt.xticks(rotation=45)
    ax.legend(['Average Milk'])
    plt.tight_layout()
    return fig