import pandas as pd
import matplotlib.pyplot as plt
import datetime

class LoanBookAnalyzer:
    def __init__(self, loan_data):
        self.loan_data = loan_data

    def calculate_percentage_recovered(self):
        self.recovered_amount = self.loan_data['recoveries'].sum()
        self.total_investor_funding = self.loan_data['funded_amount_inv'].sum()
        self.total_funded_amount = self.loan_data['funded_amount'].sum()

        self.percentage_recovered_investor_funding = (self.recovered_amount / self.total_investor_funding) * 100
        self.percentage_recovered_total_funded = (self.recovered_amount / self.total_funded_amount) * 100

    def visualize_recovery_percentage(self):
        labels = ['Recovered Amount', 'Remaining Amount']
        sizes = [self.recovered_amount, self.total_investor_funding - self.recovered_amount]
        colors = ['#ff9999', '#66b3ff']
        explode = (0.1, 0)

        plt.figure(figsize=(10, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.title('Percentage of Recovered Amount against Investor Funding')
        plt.axis('equal')
        plt.show()

    def estimate_recovery_percentage_six_months(self):
        current_loans_data = self.loan_data[self.loan_data['loan_status'] == 'Current']
        total_out_prncp = current_loans_data['out_prncp'].sum()
    
        recovery_amounts = [0] * 6
    
        for index, row in current_loans_data.iterrows():
            repayment_next_six_months = 0
            for month in range(6):
                remaining_out_prncp = max(0, row['out_prncp'] - repayment_next_six_months)
                repayment_current_month = min(row['instalment'], remaining_out_prncp * row['int_rate'] / 12)
                recovery_amounts[month] += repayment_current_month
                repayment_next_six_months += repayment_current_month
        
        total_recovery = [min(recovery_amount, total_out_prncp) for recovery_amount in recovery_amounts]
        percentage_recovered_six_months = [(recovery_amount / total_out_prncp) * 100 if total_out_prncp != 0 else 0 for recovery_amount in total_recovery]

        return total_recovery, percentage_recovered_six_months
    
    def calculate_charged_off_percentage(self):
        charged_off_loans = self.loan_data[self.loan_data['loan_status'] == 'Charged Off']
        total_loans = len(self.loan_data)
        charged_off_count = len(charged_off_loans)
        charged_off_percentage = (charged_off_count / total_loans) * 100
        return charged_off_percentage

    def calculate_total_amount_charged_off(self):
        charged_off_loans = self.loan_data[self.loan_data['loan_status'] == 'Charged Off']
        total_amount_charged_off = charged_off_loans['total_payment'].sum()
        return total_amount_charged_off

    def calculate_projected_loss_charged_off(self):
        # Convert 'issue_date' to datetime
        self.loan_data['issue_date'] = pd.to_datetime(self.loan_data['issue_date'], format='%d/%m/%Y')
        
        # Filter charged off loans
        charged_off_loans = self.loan_data[self.loan_data['loan_status'] == 'Charged Off'].copy()
        # charged_off_loans = self.loan_data[self.loan_data['loan_status'] == 'Charged Off']

        # Calculate remaining principal and loss in revenue
        charged_off_loans['remaining_principal'] = charged_off_loans['out_prncp']
        charged_off_loans['loss_in_revenue'] = charged_off_loans['remaining_principal'] + charged_off_loans['total_rec_int'] + charged_off_loans['total_rec_late_fee']

        # Calculate future issue year based on current year
        current_year = datetime.datetime.now().year
        charged_off_loans['future_issue_year'] = current_year + (charged_off_loans['issue_date'].dt.year - current_year)

        # Project loss over the remaining term of the loans
        projected_loss = charged_off_loans.groupby('future_issue_year')['loss_in_revenue'].sum()

        # Visualize the projected loss
        plt.figure(figsize=(10, 6))
        projected_loss.plot(kind='bar', color='red')
        plt.title('Projected Loss Over Remaining Term of Charged Off Loans')
        plt.xlabel('Future Year')
        plt.ylabel('Projected Loss ($)')
        plt.show()

        return projected_loss
