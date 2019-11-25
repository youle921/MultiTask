package momfo.operators.migrationselection;

import java.util.HashMap;

import momfo.util.Configuration;
import momfo.util.JMException;

/**
 * Class implementing a factory of selection operators
 */
public class migrationFactory {

	/**
	 * Gets a selection operator through its name.
	 * 
	 * @param name
	 *            of the operator
	 * @return the operator
	 * @throws JMException
	 */
	public static MigrationSelection getSelectionOperator(String name, HashMap parameters) throws JMException {
		if (name.equalsIgnoreCase("Random"))
			return new RandomSelection(parameters);
		else if (name.equalsIgnoreCase("Neighbor"))
			return new NeighborSelection(parameters);
		else {
			Configuration.logger_.severe("Operator '" + name + "' not found ");
			throw new JMException("Exception in " + name + ".getSelectionOperator()");
		} // else
	} // getSelectionOperator
} // SelectionFactory