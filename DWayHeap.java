import java.util.Arrays;
import java.util.Collection;
import java.util.LinkedList;
import java.util.NoSuchElementException;

public class DWayHeap<T extends Comparable<T>> {

    /**
     * The actual container for elements added to the heap.
     */
    private LinkedList<T> heap;

    /**
     * States the branching factor of the heap - How many child each node has.
     */
    private int branch;
    
    /**
     * If true (by default) the heap is a minheap, otherwise a maxheap. 
     */
    public boolean minheap;

    /**
     * Constructor: creates a d-way minheap.
     * 
     * @param d The branching factor for the heap
     * @throws IllegalArgumentException Iff d < 2.
     */
    public DWayHeap(Integer d) throws IllegalArgumentException {
        init(d, true, null);
    }

    /**
     * Constructor: creates a d-way heap; whether it's a minheap or a maxheap depends
     * on the second parameter.
     * 
     * @param d The branching factor for the heap
     * @param minHeap If true the heap is a minheap (smallest element at its top);
     *                Otherwise it is a maxheap.
     * @throws IllegalArgumentException Iff d < 2.
     */    
    public DWayHeap(Integer d, boolean minHeap) throws IllegalArgumentException {
        init(d, minHeap, null);
    }

    /**
     * Constructor: creates a d-way minheap from the collection passed as second argumenr,
     * using the heapify algorithm to build it in linear time.
     * 
     * @param d The branching factor for the heap.
     * @param list The initial set of elements to be contained by the heap.
     * @throws IllegalArgumentException Iff d < 2.
     */    
    public DWayHeap(Integer d, Collection<T> list)
            throws IllegalArgumentException {
        init(d, true, list);
    }

    /**
     * Constructor: creates a d-way minheap from the collection passed as second argumenr,
     * using the heapify algorithm to build it in linear time; 
     * Whether it's a minheap or a maxheap depends on the second parameter.
     *  
     * @param d The branching factor for the heap.
     * @param minHeap If true the heap is a minheap (smallest element at its top);
     *                Otherwise it is a maxheap.
     * @param list The initial set of elements to be contained by the heap.
     * @throws IllegalArgumentException Iff d < 2.
     */    
    public DWayHeap(Integer d, boolean minHeap, Collection<T> list) {
        init(d, minHeap, list);
    }

    /**
     * Helper method to allow to reuse this class both as minheap and maxheap.
     * Evaluate which of the two elements passed as parameters is the smallest.
     * 
     * @param x First input to evaluate;
     * @param y Second input to evaluate;
     * @return true <=> x is smaller than y.
     */
    private boolean lt(T x, T y) {
        return minheap ? x.compareTo(y) < 0 : x.compareTo(y) > 0;
    }

    /**
     * Helper method to allow to reuse this class both as minheap and maxheap.
     * Evaluate which of the two elements passed as parameters is the smallest.
     * 
     * @param x First input to evaluate;
     * @param y Second input to evaluate;
     * @return true <=> x is not larger than y.
     */    
    private boolean le(T x, T y) {
        return lt(x, y) || x.compareTo(y) == 0;
    }

    /**
     * Helper method: initialize the heap.
     * @param d The branching factor for the heap.
     * @param minHeap If true the heap is a minheap (smallest element at its top);
     *                Otherwise it is a maxheap.
     * @param list The initial set of elements to be contained by the heap.
     * @throws IllegalArgumentException Iff d < 2.
     */
    private void init(Integer d, boolean minHeap, Collection<T> list)
            throws IllegalArgumentException {
        if (d < 2) {
            throw new IllegalArgumentException("Branching factor must be 2 or greater");
        }
        this.minheap = minHeap;
        this.branch = d;
        if (list != null && !list.isEmpty()) {
            heapify(list);
        } else {
            heap = new LinkedList<T>();
        }
    }

    /**
     * Given a position inside the heap, returns the index of its parent.
     * @param child The index of the element whose parent is required.
     * @return i >= 0 if child has a parent, -1 otherwise.
     */
    private int parentIndex(int child) {
        if (child == 0)
            return -1;
        else
            return (child - 1) / branch; // auto floor
    }

    /**
     * Given a position inside the heap, returns the index of its leftmost child.
     * This index might or might not be inside the heap - no check is performed at this stage.
     * @param parent The index of the element whose children must be located.
     * @return The index of the first child of the element passed.
     */
    private int childIndex(int parent) {
        return parent * branch + 1;
    }

    /**
     * Build a heap from a collection of elements, in linear worst case time.
     * Running time: O(n) in the worst case.
     * @param list The collection to be inserted in the heap.
     */
    private void heapify(Collection<T> list) {
        heap = new LinkedList<T>(list);
        
        int child, parent;
        T tmp;
        for (child = heap.size() - 1; child > 0; child--) {
            parent = this.parentIndex(child);
            if (this.lt(heap.get(child), heap.get(parent))) {
                tmp = heap.get(child);
                heap.set(child, heap.get(parent));
                heap.set(parent, tmp);
            }
        }
    }

    /**
     * Remove the top element from the heap, and returns it.
     * The top element is guaranteed to be the maximum in a maxheap, 
     * and the minimum in a minheap.
     * Running time: O(log_d(n)) in the worst case.
     * @return The top element in the heap, if it isn't empty.
     * @throws NoSuchElementException If the heap is empty.
     */
    public T remove() throws NoSuchElementException {
        T res = heap.getFirst(); // Stores the top element without removing it

        if (heap.size() == 1) {
            heap.removeFirst(); // Only one element
            return res;
        }
        T parentElem, bestChildElem;
        parentElem = heap.removeLast();

        int i, parent = 0, child = 1, bestChild;

        while (child < heap.size()) {

            bestChild = child;
            bestChildElem = heap.get(child);
            for (i = 1; i < branch && child + i < heap.size(); i++) {
                if (lt(heap.get(child + i), bestChildElem)) {
                    bestChild = child + i;
                    bestChildElem = heap.get(bestChild);
                }
            }
            if (lt(parentElem, bestChildElem)) {
                heap.set(parent, parentElem);
                return res; // The heap properties have been restored
            } else {
                heap.set(parent, bestChildElem);
                parent = bestChild;
                child = this.childIndex(parent);
            }
        }
        heap.set(parent, parentElem);
        return res;
    }

    /**
     * Add a new element to the heap, ensuring that the heap properties are not violated.
     * Running time: O(log_d(n)) in the worst case.
     * @param el The new element to be added.
     * @return This heap object, to allow method chaining.
     */
    public DWayHeap<T> add(T el) {
        heap.add(el);
        if (heap.size() > 1) {
            pullUp(heap.size() - 1);
        }
        return this;
    }
    
    /**
     * Helper method: climb an element towards the top of the heap until heap
     * properties are not violated anymore.
     * Running time: O(log(n)) in the worst case.
     * @param child The index of the element that need to be moved towards the top.
     */
    private void pullUp(int child) {
        T el = heap.get(child);
        
        int parent = this.parentIndex(child);
        T parentElem;
        while (parent >= 0) {
            parentElem = heap.get(parent);
            if (lt(el, parentElem)) {
                heap.set(child, parentElem);
                child = parent;
                parent = this.parentIndex(parent);
            } else {
                break;
            }
        }
        heap.set(child, el);        
    }
    
    /**
     * Decrease the priority of an element in the heap: it replaces one element of type T
     * with another one, which must be smaller [greater, for a maxheap]. 
     * Running time: O(log_d(n)) in the worst case.
     * @param oldElement The element to be replaced.
     * @param newElement The new element with whom the old one must be replaced. 
     *                   It must have a lower priority than the old one
     *                   (hence be smaller if it is a minheap, larger in a maxheap).
     * @return This heap object, to allow method chaining.
     * @throws NoSuchElementException If oldElement is not in the heap.
     * @throws IllegalArgumentException If the new element is greater [smaller, 
     *                                  for a maxheap] than the old one.
     */
    public DWayHeap<T> decreasePriority(T oldElement, T newElement) throws NoSuchElementException, IllegalArgumentException {
        if (lt(oldElement, newElement)) {
            throw new IllegalArgumentException();
        }
        int child = this.heap.indexOf(oldElement);
        
        if (child == -1) throw new NoSuchElementException();
        heap.set(child, newElement);
        pullUp(child);
        
        return this;
    }

    /**
     * Check that whether the heap contains at least one element.
     * @return True <=> the heap contains at least one element.
     */
    public boolean isEmpty() {
        return heap.isEmpty();
    }

    /**
     * Asserts the properties of the heap.
     */
    private void checkHeapProperties() {
        if (isEmpty()) {
            assert (heap.size() == 0);
        }

        int parent = 0, child = 1;

        while (child < heap.size()) {
            for (int i = 0; i < branch && child + i < heap.size(); i++) {
                try {
                    assert (le(heap.get(parent), heap.get(child + i)));
                } catch (AssertionError e) {
                    System.out.println(branch);
                    System.out.println(parent + " " + (child + i));
                    System.out.println(heap);
                    throw e;
                }
            }
            parent += 1;
            child = branch * parent + 1;
        }
    }
    
    
    /**
     * Tests the class
     */
    private static void test() {
        boolean exceptionThrown = false;
        
        //Branching factor must be >= 2
        try {
            new DWayHeap<Integer>(1);
        } catch (IllegalArgumentException e) {
            exceptionThrown = true;
        }
        assert (exceptionThrown);
        try {
            new DWayHeap<Integer>(-1);
        } catch (IllegalArgumentException e) {
            exceptionThrown = true;
        }
        assert (exceptionThrown);        

        //Test lt and le helper methods for minheaps and maxheaps
        DWayHeap<Integer> testHeap = new DWayHeap<Integer>(2);
        assert (testHeap.lt(1, 2));
        assert (testHeap.le(1, 1));
        assert (!testHeap.lt(2, 1));

        testHeap = new DWayHeap<Integer>(2, false);
        assert (testHeap.lt(2, 1));
        assert (testHeap.le(1, 1));
        assert (!testHeap.lt(1, 2));

        LinkedList<Integer> stack;

        // Min heap, branch factor d
        for (int d = 2; d < 7; d++) {
            stack = new LinkedList<Integer>();
            testHeap = new DWayHeap<Integer>(2);

            assert (testHeap.isEmpty());

            exceptionThrown = false;
            try {
                testHeap.remove();
            } catch (NoSuchElementException e) {
                exceptionThrown = true;
            }
            assert (exceptionThrown);

            testHeap.add((int) (Math.random() * 100));
            assert (!testHeap.isEmpty());
            for (int i = 0; i < 100 + (int) (50 * Math.random()); i++) {
                testHeap.add((int) (Math.random() * 100));
                
                testHeap.checkHeapProperties();
                if (Math.random() < 0.15) {
                    testHeap.remove();
                    testHeap.checkHeapProperties();
                }
            }

            stack.add(Integer.MIN_VALUE);

            while (!testHeap.isEmpty()) {
                int tmp = testHeap.remove();
                assert (tmp >= stack.getLast());
                stack.addLast(tmp);
            }
        }

        // Max heap, branch factor d
        for (int d = 2; d < 7; d++) {
            stack = new LinkedList<Integer>();
            testHeap = new DWayHeap<Integer>(2, false);

            assert (testHeap.isEmpty());

            exceptionThrown = false;
            try {
                testHeap.remove();
            } catch (NoSuchElementException e) {
                exceptionThrown = true;
            }
            assert (exceptionThrown);

            testHeap.add((int) (Math.random() * 100));
            assert (!testHeap.isEmpty());
            for (int i = 0; i < 100 + (int) (50 * Math.random()); i++) {
                testHeap.add((int) (Math.random() * 100));
                if (Math.random() < 0.15) {
                    testHeap.remove();
                    testHeap.checkHeapProperties();
                }
            }

            stack.add(Integer.MAX_VALUE);

            while (!testHeap.isEmpty()) {
                int tmp = testHeap.remove();
                try {
                    assert (tmp <= stack.getLast());
                } catch (AssertionError e) {
                    System.out.println(testHeap.heap);
                    throw e;
                }
                stack.addLast(tmp);
            }
        }
        // Test heapify
        DWayHeap<Double> testHeapDouble = new DWayHeap<Double>(3,
                Arrays.asList(new Double[] { 0.1, 4.0, 1.321, 3.1415, -7.1 }));
        testHeapDouble.checkHeapProperties();
        for (int i = 0; i < 50; i++) {
            testHeapDouble.add(Math.random());
        }
        testHeapDouble.checkHeapProperties();
        
        testHeapDouble = new DWayHeap<Double>(4, null);
        testHeapDouble.checkHeapProperties();
        for (int i = 0; i < 50; i++) {
            testHeapDouble.add(Math.random());
        }
        testHeapDouble.checkHeapProperties();
        
        testHeapDouble = new DWayHeap<Double>(3, false,
                Arrays.asList(new Double[] { 0.1, 4.0, 1.321, 3.1415, -7.1 }));
        testHeapDouble.checkHeapProperties();
        testHeapDouble.decreasePriority(4.0, 8.0);
        for (int i = 0; i < 50; i++) {
            testHeapDouble.add(Math.random());
        }
        testHeapDouble.checkHeapProperties();
        
        testHeap = new DWayHeap<Integer>(4);
        
        for (Integer i : new Integer[]{3, 1, 5, 2, 4, 6, 8, 7, 0}){
            testHeap.add(i);
        }
        
        int j = 0;
        for (int i = 0; i < 9; i++) {
            try {
                j = testHeap.remove();
                assert(j == i);
            } catch(AssertionError e) {
                System.out.println(i + " " + j);
                System.out.println(testHeap.heap);
                throw e;
            }
        }
    }

    /**
     * @param args
     */
    public static void main(String[] args) {
        test();
    }

}
