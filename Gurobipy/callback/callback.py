import sys
import gurobipy as GRB
def mycallback(model,where):
	if where==GRB.Callback.POLLING:
		pass
	elif where==GRB.Callback.PRESOLVE:
		cdels=model.cbGet(GRB.Callback.PRE_COLDEL)
		rdels=model.cbGet(GRB.Callback.PRE_ROWDEL)
		if cdels or rdels:
			print('%d columns and %d rows are removed'%(cdels,rdels))
	elif where ==GRB.Callback.SIMPLEX:
		itcnt=model.cbGet(GRB.Callback.SPX_ITRCNT)
		if itcnt-model._lastiter>=100:
			model._lastiter=itcnt
			obj=model.cbGet(GRB.Callback.SPX_OBJVAL)
			ispert=model.cbGet(GRB.Callback.SPX_ISPERT)
			pinf=model.cbGet(GRB.Callback.SPX_PRIMINF)
			dinf=model.cbGet(GRB.Callback.SPX_DUALINF)
			if ispert==0:
				ch=' '
			elif ispert==1:
				ch='S'
			else:
				ch='P'
			print('%d %g%s %g %g' % (int(itcnt),obj,ch,pinf,dinf))
	elif where ==GRB.Callback.MIP:
		nodecnt = model.cbGet(GRB.Callback.MIP_NODCNT)
		objbst = model.cbGet(GRB.Callback.MIP_OBJBST)
		objbnd = model.cbGet(GRB.Callback.MIP_OBJBND)
		solcnt = model.cbGet(GRB.Callback.MIP_SOLCNT) 
		if nodecnt - model._lastnode >= 100:
			model._lastnode = nodecnt
			actnodes = model.cbGet(GRB.Callback.MIP_NODLFT) 
			itcnt = model.cbGet(GRB.Callback.MIP_ITRCNT)
			cutcnt = model.cbGet(GRB.Callback.MIP_CUTCNT) 
			print('%d %d %d %g %g %d %d' % (nodecnt, actnodes, \
				itcnt, objbst, objbnd, solcnt, cutcnt))
		if abs(objbst - objbnd) < 0.1 * (1.0 + abs(objbst)):
			print('Stop early - 10% gap achieved')
			model.terminate()
		if nodecnt >= 10000 and solcnt:
			print('Stop early - 10000 nodes explored')
			model.terminate()
	elif where == GRB.Callback.MIPSOL:
		# MIP solution callback
		nodecnt = model.cbGet(GRB.Callback.MIPSOL_NODCNT) 
		obj = model.cbGet(GRB.Callback.MIPSOL_OBJ)
		solcnt = model.cbGet(GRB.Callback.MIPSOL_SOLCNT) 
		x = model.cbGetSolution(model._vars)
		print('**** New solution at node %d, obj %g, sol %d, ' \
				'x[0] = %g ****' % (nodecnt, obj, solcnt, x[0]))
	elif where == GRB.Callback.MIPNODE:
		# MIP node callback
		print('**** New node ****')
		if model.cbGet(GRB.Callback.MIPNODE_STATUS) == GRB.Status.OPTIMAL:
			x = model.cbGetNodeRel(model._vars)
			model.cbSetSolution(model.getVars(), x) 
	elif where == GRB.Callback.BARRIER:
		# Barrier callback
		itcnt = model.cbGet(GRB.Callback.BARRIER_ITRCNT) 
		primobj = model.cbGet(GRB.Callback.BARRIER_PRIMOBJ) 
		dualobj = model.cbGet(GRB.Callback.BARRIER_DUALOBJ) 
		priminf = model.cbGet(GRB.Callback.BARRIER_PRIMINF) 
		dualinf = model.cbGet(GRB.Callback.BARRIER_DUALINF) 
		cmpl = model.cbGet(GRB.Callback.BARRIER_COMPL) 
		print('%d %g %g %g %g %g'%(itcnt, primobj, dualobj,priminf, dualinf, cmpl))
	elif where == GRB.Callback.MESSAGE:
		# Message callback
		msg = model.cbGet(GRB.Callback.MSG_STRING) 
		model._logfile.write(msg)
		
if len(sys.argv) < 2:
	print('Usage: callback.py filename') 
	quit()
# Turn off display and heuristics
GRB.setParam('OutputFlag', 0)
GRB.setParam('Heuristics', 0)
# Read model from file
model = GRB.read(sys.argv[1])
# Open log file
logfile = open('cb.log', 'w')
# Pass data into my callback function
model._lastiter = -GRB.INFINITY 
model._lastnode = -GRB.INFINITY 
model._logfile = logfile 
model._vars = model.getVars()
# Solve model and capture solution information
model.optimize(mycallback)

print('')
print('Optimization complete') 
if model.SolCount == 0:
	print('No solution found, optimization status = %d' % model.Status) 
else:
	print('Solution found, objective = %g' % model.ObjVal) 
	for v in model.getVars():
		if v.X != 0.0:
			print('%s %g' % (v.VarName, v.X))
# Close log file
logfile.close()
