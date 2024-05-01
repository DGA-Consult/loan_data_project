import matplotlib.pyplot as plt

class LoanBookAnalyzer:
    def __init__(self, loan_data):
        self.loan_data = loan_data
        ## Create a new DataFrame with only the specified columns
        # selected_columns = self.loan_data[['recoveries', 'funded_amount_inv', 'funded_amount']]
        # Print the first few rows of the selected columns
        # print("First few rows of selected columns:")
        # print(selected_columns.head())

    def calculate_percentage_recovered(self):
        self.recovered_amount = self.loan_data['recoveries'].sum()
        self.total_investor_funding = self.loan_data['funded_amount_inv'].sum()
        self.total_funded_amount = self.loan_data['funded_amount'].sum()

        self.percentage_recovered_investor_funding = (self.recovered_amount / self.total_investor_funding) * 100
        self.percentage_recovered_total_funded = (self.recovered_amount / self.total_funded_amount) * 100

        return None

    def visualize_recovery_percentage(self):
        # percentage_recovered_investor_funding, percentage_recovered_total_funded = self.calculate_percentage_recovered()

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
        # Filter for loans where 'loan_status' is 'Current'
        current_loans_data = self.loan_data[self.loan_data['loan_status'] == 'Current']
    
        # Calculate the total amount of 'out_prncp' for current loans
        total_out_prncp = current_loans_data['out_prncp'].sum()
    
        # Initialize lists to store recovery amounts for each month
        recovery_amounts = [0] * 6
    
        # Calculate the total amount to be repaid in the next 6 months for each loan
        for index, row in current_loans_data.iterrows():
            # Calculate repayment for each month based on 'instalment' - 'out_prncp' * 'int_rate' / 12
            repayment_next_six_months = 0
            for month in range(6):
                # Calculate the remaining amount to be repaid for the current month
                remaining_out_prncp = max(0, row['out_prncp'] - repayment_next_six_months)
            
                # Calculate the repayment for the current month
                repayment_current_month = min(row['instalment'], remaining_out_prncp * row['int_rate'] / 12)
            
                # Add the repayment for the current month to the total for the next six months
                recovery_amounts[month] += repayment_current_month
            
                # Update the total repayment for the next six months
                repayment_next_six_months += repayment_current_month
        
        # Calculate the total recovery across all loans for each month
        total_recovery = [min(recovery_amount, total_out_prncp) for recovery_amount in recovery_amounts]
    
        # Calculate the percentage of the total 'out_prncp' recovered for each month
        percentage_recovered_six_months = [(recovery_amount / total_out_prncp) * 100 if total_out_prncp != 0 else 0 for recovery_amount in total_recovery]

        # Print the amount and percentage of the total 'out_prncp' recovered for each month
        for month, (recovery_amount, percentage) in enumerate(zip(total_recovery, percentage_recovered_six_months), start=1):
            print(f"Month {month}: Total Recovery Amount: ${recovery_amount:.2f}, Percentage of Total 'out_prncp' Recovered: {percentage:.2f}%")
    
        return percentage_recovered_six_months
    
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