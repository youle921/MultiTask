package momfo.problems.base;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Map;

import momfo.core.Problem;
import momfo.core.Solution;
import momfo.core.Variable;
import momfo.util.JMException;

public class Knapsack extends Problem{



	private static int[][] profit_;
	private static int[][] weight_;

	static int NumberOfItems_;
	static int NumberOfKnapsack_;

	static double[] capacity_;

	int decodeType = 0;//

	public  void setDecodeType(int d ){
		decodeType = d;
	}

	public Knapsack(Integer numberOfVariables, Integer numberOfObjectives) {
		numberOfVariables_ = numberOfVariables;
		numberOfObjectives_ = numberOfObjectives;
		problemName_ = "Knapsack";
	}

	public Knapsack(String filename){
		String name = filename;

		FileReading(name);
		numberOfVariables_ = NumberOfItems_;
		numberOfObjectives_ = NumberOfKnapsack_;
		problemName_ = "Knapsack";
		sort_min_= new int[NumberOfItems_];
		q_		 = new double[NumberOfItems_];
//		variableType_ = 1;

		double max;

		for(int i=0;i<NumberOfItems_;i++){
			sort_min_[i] = i;
			max = (double)profit_[0][i]/weight_[0][i];
			for(int j=1;j< 2;j++){
					max =Math.max(max,(double)profit_[j][i]/weight_[j][i]);
			}
			q_[i] = max;
		}
		int em;

		for(int i=0;i<NumberOfItems_;i++){
			for(int j=0;j<NumberOfItems_;j++){
				if(q_[sort_min_[i]] < q_[sort_min_[j]]){
					em = sort_min_[j];
					sort_min_[j] = sort_min_[i];
					sort_min_[i] = em;
				}
			}
		}

		lowerLimit_ = new double[numberOfVariables_];
		upperLimit_ = new double[numberOfVariables_];
		for (int var = 0; var < numberOfVariables_; var++) {
			lowerLimit_[var] = 0.0;
			upperLimit_[var] = 1.0;
		} // for

	}

	public static void main(String[] args){
		String 	knapsackfileName  = "Data/KnapsackData/knapsack_2_500to6.txt";

		Knapsack a = new Knapsack(knapsackfileName);

		Solution d = new Solution();

		for (int i=0;i<250;i++){
	//		d.setValue(i*2, 1);
	//		d.setValue(i*2+1, 1);
		}
		a.subscript();
	//	a.repair(d,null);
//		a.evaluate(d);
		for (int i=0;i<2;i++){
			System.out.print(d.getObjective(i) + "	" );
		}
	}
	public int[] decodeSolution(Solution sol) throws JMException{
		Variable[] decisionVariables = sol.getDecisionVariables();
		int[] x = new int[numberOfVariables_];

		for (int i = 0; i < numberOfVariables_; i++)
			if(decisionVariables[i].getValue() < 0.5){
				x[i] = 0;
			} else if (decisionVariables[i].getValue() >= 0.5){
				x[i] = 1;
			}

		return x;


	}

	public void evaluate(Solution solution) throws JMException {
		int [] val = decodeSolution(solution);

		int[] f = new int[NumberOfKnapsack_];

		int sum;
		for(int i=0;i<NumberOfKnapsack_;i++){
			sum =0;
			for(int j=0;j<NumberOfItems_;j++){
				sum += profit_[i][j]*val[j];
			}
			f[i] = sum;
		}

		break_knapsack(val);

		for (int i = 0; i < numberOfObjectives_; i++)
			solution.setObjective(i, f[i]);

 }

	//this method read the knapsack data
	public static void FileReading(String name){
		try(BufferedReader br = new BufferedReader(new FileReader(name))){
			String line = br.readLine();
			NumberOfItems_ = Integer.valueOf(line);

			line = br.readLine();
			NumberOfKnapsack_ = Integer.valueOf(line);
			profit_ = new int [NumberOfKnapsack_][NumberOfItems_];
			weight_ = new int [NumberOfKnapsack_][NumberOfItems_];
			capacity_ = new double [NumberOfKnapsack_];

			for(int i=0;i<NumberOfKnapsack_;i++){
				line = br.readLine();
				capacity_[i] = Double.parseDouble(line);
				for(int j=0;j<NumberOfItems_;j++){
					line = br.readLine();
					weight_[i][j] = Integer.valueOf(line);
					line = br.readLine();
					profit_[i][j] = Integer.valueOf(line);
				}
			}
		} catch (IOException e){
			e.printStackTrace();
		}
	}

	int[] sort_min_;
	double[]	q_;

	public void repair(Solution c,Map<String, Object> a) throws JMException {
		int[] d = new int[1];
		if( !break_knapsack(d))
			return ;
		int counter = 0;
		do {
//			d.setValue(sort_min_[counter++], 0.0);
		}while(break_knapsack(d));

	}


/*
 *  if at least one Knapsack is broken, this method return true;
 *  else return false;
 */
	public boolean break_knapsack(int[] sol ) throws JMException{
		double sum = 0;
		int bit = 1;

		for(int i =0 ;i<NumberOfKnapsack_;i++){
			sum = 0;
			for(int j=0;j<NumberOfItems_;j++){

				if(sol[j] > 0.99){
					bit = 1;
				} else if  (sol[j] < 0.01){
					bit = 0;
				}
				sum += bit*weight_[i][j];
			}
			if(sum > capacity_[i]){
				return true;
			}
		}
		return false;
	}


	public void subscript(){
		System.out.println("knapsack Capa : " + NumberOfKnapsack_);
		System.out.println("knapsack detail information : ");
		for(int i=0;i<NumberOfKnapsack_;i++){
			System.out.println("knapsack Capa : " + capacity_[i]);
	//		for(int j=0;j<NumberOfItems_;j++){
	//			System.out.println("Number" +j +"Item profit : " + profit_[i][j] + "  weight : " + weight_[i][j]);
	//			}
		}
	}


}
