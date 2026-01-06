interface FilterControlsProps {
  search: string;
  completedFilter: string;
  priorityFilter: string;
  sortFilter: string;
  onSearchChange: (value: string) => void;
  onCompletedChange: (value: string) => void;
  onPriorityChange: (value: string) => void;
  onSortChange: (value: string) => void;
}

export default function FilterControls({
  search,
  completedFilter,
  priorityFilter,
  sortFilter,
  onSearchChange,
  onCompletedChange,
  onPriorityChange,
  onSortChange
}: FilterControlsProps) {
  return (
    <div className="mb-6 p-6 bg-gradient-to-br from-gray-900 to-blue-950 rounded-xl shadow-xl border border-gray-800">
      <h2 className="text-2xl font-bold mb-4 text-white">Filters & Sorting</h2>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Search Input */}
        <div>
          <label
            htmlFor="search"
            className="block text-sm font-semibold text-white mb-2"
          >
            Search
          </label>
          <input
            type="text"
            id="search"
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-600"
            placeholder="Search tasks..."
          />
        </div>

        {/* Completion Status Filter */}
        <div>
          <label
            htmlFor="completed"
            className="block text-sm font-semibold text-white mb-2"
          >
            Status
          </label>
          <select
            id="completed"
            value={completedFilter}
            onChange={(e) => onCompletedChange(e.target.value)}
            className="w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
          >
            <option value="">All</option>
            <option value="true">Completed</option>
            <option value="false">Incomplete</option>
          </select>
        </div>

        {/* Priority Filter */}
        <div>
          <label
            htmlFor="priority"
            className="block text-sm font-semibold text-white mb-2"
          >
            Priority
          </label>
          <select
            id="priority"
            value={priorityFilter}
            onChange={(e) => onPriorityChange(e.target.value)}
            className="w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
          >
            <option value="">All Priorities</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>

        {/* Sort Options */}
        <div>
          <label
            htmlFor="sort"
            className="block text-sm font-semibold text-white mb-2"
          >
            Sort By
          </label>
          <select
            id="sort"
            value={sortFilter}
            onChange={(e) => onSortChange(e.target.value)}
            className="w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
          >
            <option value="">Default (Newest First)</option>
            <option value="created_at">Date Created</option>
            <option value="priority">Priority</option>
            <option value="title">Title</option>
          </select>
        </div>
      </div>

      {/* Active Filters Display */}
      {(search || completedFilter || priorityFilter || sortFilter) && (
        <div className="mt-4 pt-4 border-t border-gray-700">
          <div className="text-sm text-gray-300 mb-2">Active filters:</div>
          <div className="flex flex-wrap gap-2">
            {search && (
              <span className="px-3 py-1 bg-blue-700 text-white rounded-full text-xs font-semibold">
                Search: {search}
              </span>
            )}
            {completedFilter && (
              <span className="px-3 py-1 bg-blue-700 text-white rounded-full text-xs font-semibold">
                Status: {completedFilter === 'true' ? 'Completed' : 'Incomplete'}
              </span>
            )}
            {priorityFilter && (
              <span className="px-3 py-1 bg-blue-700 text-white rounded-full text-xs font-semibold">
                Priority: {priorityFilter}
              </span>
            )}
            {sortFilter && (
              <span className="px-3 py-1 bg-blue-700 text-white rounded-full text-xs font-semibold">
                Sort: {sortFilter}
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
