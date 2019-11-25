package momfo.operators.migrationselection;

import java.util.HashMap;

import momfo.core.Operator;
import momfo.core.SolutionSet;

/**
 * This class represents the super class of all the migration selection operators
 */
public abstract class MigrationSelection extends Operator {

    public MigrationSelection(HashMap<String, Object> parameters) {
		super(parameters);
		// TODO Auto-generated constructor stub
	}

	abstract public void setDestinationSolution(SolutionSet solution);

} // Selection
